"""
Advanced NLP-based Resume Analyzer for Cognitive Career Recommendation System
"""

import pandas as pd
import numpy as np
import re
from datetime import datetime, timezone
from collections import Counter
import PyPDF2
from docx import Document
import json
from typing import Dict, List, Any, Tuple, Optional

# Dependency Management
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
    import nltk
    from nltk.corpus import stopwords
    from nltk.tokenize import word_tokenize, sent_tokenize
    NLTK_AVAILABLE = True
except ImportError:
    NLTK_AVAILABLE = False

class ResumeAnalyzer:
    """
    Advanced NLP Resume Analyzer using spaCy and other NLP libraries.
    Extracts skills, experience, education, and interests from documents.
    """
    
    def __init__(self):
        # 1. Initialize spaCy
        self.nlp = None
        if SPACY_AVAILABLE:
            try:
                self.nlp = spacy.load("en_core_web_sm")
            except OSError:
                self.nlp = None
        
        # 2. Initialize NLTK
        self.stop_words = set()
        if NLTK_AVAILABLE:
            try:
                nltk.download('punkt', quiet=True)
                nltk.download('stopwords', quiet=True)
                self.stop_words = set(stopwords.words('english'))
            except Exception:
                pass
        
        # 3. Load Taxonomies
        self._load_skill_patterns()
        self._load_education_patterns()
        self._load_experience_patterns()
    
    def _load_skill_patterns(self):
        self.technical_skills = {
            'programming_languages': ['python', 'java', 'javascript', 'c++', 'c#', 'ruby', 'php', 'swift', 'kotlin', 'go', 'rust', 'sql'],
            'frameworks': ['react', 'angular', 'vue', 'django', 'flask', 'spring boot', 'node.js', 'tensorflow', 'pytorch'],
            'cloud_devops': ['aws', 'azure', 'google cloud', 'docker', 'kubernetes', 'terraform', 'jenkins', 'ci/cd'],
            'data': ['machine learning', 'deep learning', 'data analysis', 'nlp', 'tableau', 'power bi', 'excel']
        }
        self.soft_skills = ['leadership', 'communication', 'teamwork', 'problem solving', 'agile', 'project management']
        
        # Canonical Lookup
        self.skill_lookup = {}
        for category in self.technical_skills.values():
            for s in category: self.skill_lookup[s.lower()] = s
        for s in self.soft_skills: self.skill_lookup[s.lower()] = s

    def _load_education_patterns(self):
        self.degree_patterns = [r'bachelor', r'master', r'ph\.?d', r'b\.?s\.?', r'm\.?s\.?']
        self.field_patterns = ['computer science', 'engineering', 'business', 'data science', 'mathematics']

    def _load_experience_patterns(self):
        self.job_title_patterns = ['engineer', 'scientist', 'manager', 'developer', 'analyst', 'lead', 'senior']

    def extract_information(self, file) -> Dict[str, Any]:
        """Main entry point for file processing"""
        text = self._extract_text_from_file(file)
        if not text:
            return {'error': 'Could not extract text from file'}
        
        return {
            'personal_info': self._extract_personal_info(text),
            'skills': self._extract_skills(text),
            'experience': self._extract_experience(text),
            'education': self._extract_education(text),
            'interests': self._extract_interests(text),
            'summary_stats': self._generate_profile_summary(text),
            'nlp_analysis': self._perform_nlp_analysis(text) if self.nlp else "NLP Model Unavailable"
        }

    def _extract_text_from_file(self, file) -> str:
        filename = getattr(file, 'filename', '').lower()
        try:
            if filename.endswith('.pdf'):
                reader = PyPDF2.PdfReader(file)
                return " ".join([page.extract_text() or '' for page in reader.pages])
            elif filename.endswith('.docx'):
                doc = Document(file)
                return "\n".join([p.text for p in doc.paragraphs])
            else:
                content = file.read()
                return content.decode('utf-8', errors='ignore') if isinstance(content, bytes) else str(content)
        except Exception as e:
            return f"Error: {str(e)}"

    def _extract_personal_info(self, text: str) -> Dict[str, str]:
        email = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
        phone = re.findall(r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', text)
        return {
            'email': email[0] if email else '',
            'phone': phone[0] if phone else '',
            'linkedin': re.search(r'linkedin\.com/in/[A-Za-z0-9-]+', text).group(0) if re.search(r'linkedin\.com/in/[A-Za-z0-9-]+', text) else ''
        }

    def _extract_skills(self, text: str) -> Dict[str, List[str]]:
        text_l = text.lower()
        results = {'technical': [], 'soft': [], 'confidence': {}}
        
        for cat, skills in self.technical_skills.items():
            for s in skills:
                if re.search(r'\b' + re.escape(s) + r'\b', text_l):
                    results['technical'].append(s)
                    results['confidence'][s] = min(1.0, len(re.findall(re.escape(s), text_l)) * 0.2)
        
        for s in self.soft_skills:
            if re.search(r'\b' + re.escape(s) + r'\b', text_l):
                results['soft'].append(s)
        
        return results

    def _extract_experience(self, text: str) -> List[Dict[str, Any]]:
        current_year = datetime.now(timezone.utc).year
        ranges = re.findall(r'((?:19|20)\d{2})\s*[-–]\s*((?:19|20)\d{2}|present|current)', text.lower())
        total = sum([max(1, (current_year if r[1] in ('present', 'current') else int(r[1])) - int(r[0])) for r in ranges])
        
        return [{
            'total_years': total,
            'titles': [t for t in self.job_title_patterns if t in text.lower()]
        }]

    def _perform_nlp_analysis(self, text: str) -> Dict[str, Any]:
        if not self.nlp: return {}
        doc = self.nlp(text[:100000]) # Safety cap
        return {
            'entities': {ent.label_: ent.text for ent in doc.ents},
            'noun_chunks': [chunk.text for chunk in list(doc.noun_chunks)[:15]]
        }

    def _generate_profile_summary(self, text: str) -> Dict[str, Any]:
        words = re.findall(r'\w+', text)
        return {
            'word_count': len(words),
            'sentiment': TextBlob(text).sentiment.polarity if TEXTBLOB_AVAILABLE else 0.0
        }

    def _extract_education(self, text: str) -> Dict[str, List[str]]:
        text_l = text.lower()
        return {
            'degrees': list(set(re.findall(r'|'.join(self.degree_patterns), text_l))),
            'fields': [f for f in self.field_patterns if f in text_l]
        }

    def _extract_interests(self, text: str) -> List[str]:
        keywords = ['ai', 'blockchain', 'gaming', 'photography', 'travel', 'open source']
        return [k for k in keywords if k in text.lower()]