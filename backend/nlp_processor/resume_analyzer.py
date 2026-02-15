"""
NLP-based Resume Analyzer for Cognitive Career Recommendation System
Handles resume parsing, skill extraction, and interest analysis using NLP techniques
"""

import pandas as pd
import numpy as np
import re
from collections import Counter
import PyPDF2
from docx import Document

# Optional NLP/ML imports - may not be available in production
try:
    import spacy
    SPACY_AVAILABLE = True
except ImportError:
    SPACY_AVAILABLE = False

try:
    from textblob import TextBlob
    TEXTBLOB_AVAILABLE = True
except ImportError:
    TEXTBLOB_AVAILABLE = False

try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False

try:
    import nltk
    from nltk.corpus import stopwords
    from nltk.tokenize import word_tokenize, sent_tokenize
    NLTK_AVAILABLE = True
except ImportError:
    NLTK_AVAILABLE = False
    stopwords = None
    word_tokenize = None
    sent_tokenize = None

from typing import Dict, List, Any, Tuple, Optional
import json

class ResumeAnalyzer:
    """
    Advanced NLP Resume Analyzer using spaCy and other NLP libraries
    Extracts skills, experience, education, and interests from resume documents
    """
    
    def __init__(self):
        # Load spaCy model
        if SPACY_AVAILABLE:
            try:
                self.nlp = spacy.load("en_core_web_sm")
            except OSError:
                print("spaCy model not found. Please install with: python -m spacy download en_core_web_sm")
                self.nlp = None
        else:
            self.nlp = None
        
        # Download NLTK data if needed
        if NLTK_AVAILABLE:
            try:
                nltk.data.find('tokenizers/punkt')
                nltk.data.find('corpora/stopwords')
            except LookupError:
                try:
                    nltk.download('punkt')
                    nltk.download('stopwords')
                except:
                    pass
            
            try:
                self.stop_words = set(stopwords.words('english'))
            except:
                self.stop_words = set()
        else:
            self.stop_words = set()
        
        # Load skill taxonomies and patterns
        self._load_skill_patterns()
        self._load_education_patterns()
        self._load_experience_patterns()
    
    def _load_skill_patterns(self):
        """Load predefined skill patterns and taxonomies"""
        self.technical_skills = {
            'programming_languages': [
                'python', 'java', 'javascript', 'c++', 'c#', 'ruby', 'php', 'swift',
                'kotlin', 'go', 'rust', 'scala', 'r', 'matlab', 'sql', 'html', 'css'
            ],
            'frameworks_libraries': [
                'react', 'angular', 'vue', 'django', 'flask', 'spring', 'node.js',
                'tensorflow', 'pytorch', 'scikit-learn', 'pandas', 'numpy', 'express'
            ],
            'databases': [
                'mysql', 'postgresql', 'mongodb', 'redis', 'elasticsearch', 'cassandra',
                'oracle', 'sqlite', 'dynamodb', 'neo4j'
            ],
            'cloud_platforms': [
                'aws', 'azure', 'google cloud', 'heroku', 'digitalocean', 'docker',
                'kubernetes', 'terraform'
            ],
            'data_science': [
                'machine learning', 'deep learning', 'data analysis', 'statistics',
                'data visualization', 'big data', 'nlp', 'computer vision'
            ],
            'tools_software': [
                'git', 'jenkins', 'jira', 'confluence', 'slack', 'figma', 'photoshop',
                'illustrator', 'tableau', 'power bi', 'excel'
            ]
        }
        
        self.soft_skills = [
            'leadership', 'communication', 'teamwork', 'problem solving',
            'critical thinking', 'project management', 'time management',
            'adaptability', 'creativity', 'analytical thinking'
        ]
    
    def _load_education_patterns(self):
        """Load education-related patterns"""
        self.degree_patterns = [
            r'bachelor.*?of.*?science', r'b\.?s\.?', r'bachelor.*?degree',
            r'master.*?of.*?science', r'm\.?s\.?', r'master.*?degree',
            r'ph\.?d\.?', r'doctorate', r'phd', r'master.*?of.*?arts', r'm\.?a\.?',
            r'bachelor.*?of.*?arts', r'b\.?a\.?', r'associate.*?degree'
        ]
        
        self.field_patterns = [
            'computer science', 'information technology', 'engineering',
            'mathematics', 'statistics', 'business administration',
            'marketing', 'finance', 'economics', 'psychology', 'design'
        ]
    
    def _load_experience_patterns(self):
        """Load experience and job title patterns"""
        self.job_title_patterns = [
            'software engineer', 'data scientist', 'product manager', 'designer',
            'analyst', 'developer', 'consultant', 'manager', 'director',
            'architect', 'specialist', 'coordinator', 'lead', 'senior'
        ]
        
        self.experience_patterns = [
            r'(\d+)\s*years?\s*of\s*experience',
            r'(\d+)\+\s*years?',
            r'experience.*?(\d+)\s*years?',
            r'(\d+)\s*years?\s*in'
        ]
    
    def extract_information(self, file) -> Dict[str, Any]:
        """
        Main method to extract all information from resume
        
        Args:
            file: Uploaded file object (PDF, DOC, DOCX, or TXT)
            
        Returns:
            Dictionary containing extracted resume information
        """
        # Extract text from file
        text = self._extract_text_from_file(file)
        
        if not text:
            return {'error': 'Could not extract text from file'}
        
        # Apply NLP processing
        resume_data = {
            'raw_text': text,
            'personal_info': self._extract_personal_info(text),
            'skills': self._extract_skills(text),
            'experience': self._extract_experience(text),
            'education': self._extract_education(text),
            'interests': self._extract_interests(text),
            'summary': self._generate_profile_summary(text),
            'nlp_analysis': self._perform_nlp_analysis(text)
        }
        
        return resume_data
    
    def _extract_text_from_file(self, file) -> str:
        """Extract text content from different file formats"""
        filename = file.filename.lower()
        
        try:
            if filename.endswith('.pdf'):
                return self._extract_from_pdf(file)
            elif filename.endswith('.docx'):
                return self._extract_from_docx(file)
            elif filename.endswith('.doc'):
                # For .doc files, you might need additional libraries like python-docx2txt
                return self._extract_from_doc(file)
            elif filename.endswith('.txt'):
                return file.read().decode('utf-8')
            else:
                return ''
        except Exception as e:
            print(f"Error extracting text: {str(e)}")
            return ''
    
    def _extract_from_pdf(self, file) -> str:
        """Extract text from PDF file"""
        try:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ''
            for page in pdf_reader.pages:
                extracted = page.extract_text() or ''
                text += extracted
            return text
        except Exception:
            return ''
    
    def _extract_from_docx(self, file) -> str:
        """Extract text from DOCX file"""
        try:
            doc = Document(file)
            text = ''
            for paragraph in doc.paragraphs:
                text += paragraph.text + '\n'
            return text
        except Exception:
            return ''
    
    def _extract_from_doc(self, file) -> str:
        """Extract text from DOC file (simplified)"""
        # This would require additional libraries for proper .doc support
        return "DOC format processing requires additional setup"
    
    def _extract_personal_info(self, text: str) -> Dict[str, str]:
        """Extract personal information like name, email, phone"""
        personal_info = {}
        
        # Email extraction
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, text)
        personal_info['email'] = emails[0] if emails else ''
        
        # Phone number extraction
        phone_pattern = r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
        phones = re.findall(phone_pattern, text)
        personal_info['phone'] = ''.join(phones[0]) if phones else ''
        
        # Name extraction (first line often contains name)
        lines = text.split('\n')
        potential_name = lines[0].strip() if lines else ''
        if len(potential_name.split()) <= 3 and not '@' in potential_name:
            personal_info['name'] = potential_name
        else:
            personal_info['name'] = ''
        
        # LinkedIn URL
        linkedin_pattern = r'linkedin\.com/in/[A-Za-z0-9-]+'
        linkedin_matches = re.findall(linkedin_pattern, text)
        personal_info['linkedin'] = linkedin_matches[0] if linkedin_matches else ''
        
        return personal_info
    
    def _extract_skills(self, text: str) -> Dict[str, List[str]]:
        """Extract technical and soft skills from resume text"""
        text_lower = text.lower()
        extracted_skills = {
            'technical_skills': [],
            'soft_skills': [],
            'skill_confidence': {}
        }
        
        # Extract technical skills
        for category, skills_list in self.technical_skills.items():
            found_skills = []
            for skill in skills_list:
                pattern = r'\b' + re.escape(skill.lower()) + r'\b'
                if re.search(pattern, text_lower):
                    found_skills.append(skill)
                    # Calculate confidence based on frequency
                    count = len(re.findall(pattern, text_lower))
                    extracted_skills['skill_confidence'][skill] = min(1.0, count * 0.2)
            
            if found_skills:
                extracted_skills['technical_skills'].extend(found_skills)
        
        # Extract soft skills
        for skill in self.soft_skills:
            pattern = r'\b' + re.escape(skill.lower()) + r'\b'
            if re.search(pattern, text_lower):
                extracted_skills['soft_skills'].append(skill)
        
        # Remove duplicates
        extracted_skills['technical_skills'] = list(set(extracted_skills['technical_skills']))
        extracted_skills['soft_skills'] = list(set(extracted_skills['soft_skills']))
        
        return extracted_skills
    
    def _extract_experience(self, text: str) -> List[Dict[str, Any]]:
        """Extract work experience information"""
        experience_list = []
        
        # Extract years of experience
        total_years = 0
        for pattern in self.experience_patterns:
            matches = re.findall(pattern, text.lower())
            if matches:
                years = [int(match) for match in matches if match.isdigit()]
                if years:
                    total_years = max(years)
        
        # Extract job titles
        job_titles = []
        text_lower = text.lower()
        for title in self.job_title_patterns:
            if title in text_lower:
                job_titles.append(title.title())
        
        # Create experience entries (simplified)
        if job_titles or total_years > 0:
            experience_list.append({
                'total_years': total_years,
                'job_titles': job_titles,
                'extracted_companies': self._extract_companies(text),
                'roles_identified': len(job_titles)
            })
        
        return experience_list
    
    def _extract_companies(self, text: str) -> List[str]:
        """Extract company names (basic implementation)"""
        # This is a simplified approach - in practice, you'd use Named Entity Recognition
        lines = text.split('\n')
        potential_companies = []
        
        for line in lines:
            # Look for lines that might contain company names
            if any(keyword in line.lower() for keyword in ['inc', 'corp', 'llc', 'ltd', 'company']):
                potential_companies.append(line.strip())
        
        return potential_companies[:5]  # Return top 5 matches
    
    def _extract_education(self, text: str) -> Dict[str, Any]:
        """Extract education information"""
        education_info = {
            'degrees': [],
            'institutions': [],
            'fields_of_study': [],
            'graduation_years': []
        }
        
        text_lower = text.lower()
        
        # Extract degrees
        for pattern in self.degree_patterns:
            matches = re.findall(pattern, text_lower)
            education_info['degrees'].extend(matches)
        
        # Extract fields of study
        for field in self.field_patterns:
            if field in text_lower:
                education_info['fields_of_study'].append(field)
        
        # Extract graduation years
        year_pattern = r'(19|20)\d{2}'
        years = re.findall(year_pattern, text)
        education_info['graduation_years'] = [year for year in years if int(year) > 1990]
        
        # Clean up and remove duplicates
        education_info['degrees'] = list(set(education_info['degrees']))
        education_info['fields_of_study'] = list(set(education_info['fields_of_study']))
        
        return education_info
    
    def _extract_interests(self, text: str) -> List[str]:
        """Extract interests and hobbies"""
        interest_keywords = [
            'machine learning', 'artificial intelligence', 'data science',
            'web development', 'mobile development', 'gaming', 'photography',
            'travel', 'sports', 'music', 'reading', 'writing', 'design',
            'entrepreneurship', 'blockchain', 'cybersecurity', 'cloud computing'
        ]
        
        found_interests = []
        text_lower = text.lower()
        
        for interest in interest_keywords:
            if interest in text_lower:
                found_interests.append(interest)
        
        return found_interests
    
    def _generate_profile_summary(self, text: str) -> Dict[str, Any]:
        """Generate a summary of the resume profile"""
        # Word count and basic statistics with safe fallbacks
        try:
            if NLTK_AVAILABLE and word_tokenize and sent_tokenize:
                words = word_tokenize(text)
                sentences = sent_tokenize(text)
            else:
                raise ValueError('NLTK tokenizers unavailable')
        except Exception:
            words = re.findall(r'\b\w+\b', text)
            sentences = [s for s in re.split(r'[.!?]+', text) if s.strip()]

        avg_words_per_sentence = len(words) / max(1, len(sentences))

        noun_phrases = []
        sentiment_polarity = 0.0
        sentiment_subjectivity = 0.0

        if TEXTBLOB_AVAILABLE:
            try:
                blob = TextBlob(text)
                noun_phrases = [str(phrase) for phrase in blob.noun_phrases[:10]]
                sentiment_polarity = blob.sentiment.polarity
                sentiment_subjectivity = blob.sentiment.subjectivity
            except Exception:
                pass

        return {
            'word_count': len(words),
            'sentence_count': len(sentences),
            'avg_words_per_sentence': round(avg_words_per_sentence, 2),
            'key_phrases': noun_phrases,
            'sentiment_polarity': sentiment_polarity,
            'sentiment_subjectivity': sentiment_subjectivity
        }
    
    def _perform_nlp_analysis(self, text: str) -> Dict[str, Any]:
        """Perform advanced NLP analysis using spaCy"""
        if not self.nlp:
            return {'error': 'spaCy model not available'}
        
        # Process text with spaCy
        doc = self.nlp(text[:1000000])  # Limit text length for processing
        
        # Extract entities
        entities = {}
        for ent in doc.ents:
            entity_type = ent.label_
            if entity_type not in entities:
                entities[entity_type] = []
            entities[entity_type].append(ent.text)
        
        # Extract important tokens
        important_tokens = []
        for token in doc:
            if (token.pos_ in ['NOUN', 'PROPN', 'ADJ'] and 
                not token.is_stop and 
                not token.is_punct and 
                len(token.text) > 2):
                important_tokens.append({
                    'text': token.text,
                    'pos': token.pos_,
                    'lemma': token.lemma_
                })
        
        # Extract noun chunks
        noun_chunks = [chunk.text for chunk in doc.noun_chunks]
        
        analysis = {
            'entities': entities,
            'important_tokens': important_tokens[:50],  # Top 50 tokens
            'noun_chunks': noun_chunks[:20],  # Top 20 noun chunks
            'language_detected': doc.lang_,
            'token_count': len(doc)
        }
        
        return analysis
    
    def analyze_skill_gaps(self, user_skills: List[str], target_role: str) -> Dict[str, List[str]]:
        """
        Analyze skill gaps for a target role
        
        Args:
            user_skills: List of user's current skills
            target_role: Target job role
            
        Returns:
            Dictionary containing skill gap analysis
        """
        role_requirements = {
            'data scientist': [
                'python', 'r', 'sql', 'machine learning', 'statistics',
                'pandas', 'numpy', 'scikit-learn', 'tableau', 'aws'
            ],
            'software engineer': [
                'programming', 'algorithms', 'data structures', 'git',
                'testing', 'debugging', 'database design', 'api development'
            ],
            'product manager': [
                'product strategy', 'market research', 'analytics',
                'project management', 'stakeholder management', 'agile'
            ]
        }
        
        required_skills = role_requirements.get(target_role.lower(), [])
        user_skills_lower = [skill.lower() for skill in user_skills]
        
        skill_gaps = {
            'missing_skills': [skill for skill in required_skills if skill not in user_skills_lower],
            'matching_skills': [skill for skill in required_skills if skill in user_skills_lower],
            'additional_skills': [skill for skill in user_skills_lower if skill not in required_skills],
            'match_percentage': len([skill for skill in required_skills if skill in user_skills_lower]) / max(1, len(required_skills)) * 100
        }
        
        return skill_gaps
    
    def get_skill_recommendations(self, current_skills: List[str], target_domain: str) -> List[str]:
        """
        Recommend skills to learn based on current skills and target domain
        
        Args:
            current_skills: User's current skills
            target_domain: Target career domain
            
        Returns:
            List of recommended skills to learn
        """
        domain_skills = {
            'data_science': [
                'machine learning', 'deep learning', 'python', 'r', 'sql',
                'tableau', 'power bi', 'aws', 'spark', 'hadoop'
            ],
            'web_development': [
                'javascript', 'react', 'node.js', 'html', 'css',
                'mongodb', 'express', 'git', 'docker', 'aws'
            ],
            'mobile_development': [
                'swift', 'kotlin', 'react native', 'flutter',
                'firebase', 'android studio', 'xcode', 'git'
            ]
        }
        
        target_skills = domain_skills.get(target_domain, [])
        current_skills_lower = [skill.lower() for skill in current_skills]
        
        recommendations = [
            skill for skill in target_skills 
            if skill not in current_skills_lower
        ]
        
        return recommendations[:10]  # Top 10 recommendations