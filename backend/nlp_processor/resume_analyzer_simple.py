"""
Simplified NLP-based Resume Analyzer for Cognitive Career Recommendation System
"""

import re
from datetime import datetime, timezone
from typing import Dict, List, Any, Optional

class SimpleResumeAnalyzer:
    """
    Simplified Resume Analyzer that extracts basic information from resume text
    """
    
    def __init__(self):
        # Comprehensive skill patterns organized by category
        self.skill_patterns = {
            'programming': [
                'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'php', 'ruby', 'go', 'rust',
                'kotlin', 'swift', 'scala', 'r programming', 'perl', 'shell', 'bash', 'groovy'
            ],
            'web_frameworks': [
                'react', 'angular', 'vue', 'django', 'flask', 'fastapi', 'spring', 'spring boot',
                'express', 'node.js', 'node', 'asp.net', 'laravel', 'rails', 'nextjs', 'nuxt'
            ],
            'databases': [
                'sql', 'mysql', 'postgresql', 'mongodb', 'cassandra', 'redis', 'elasticsearch',
                'dynamodb', 'oracle', 'sqlite', 'mariadb', 'neo4j', 'graphql'
            ],
            'data_science': [
                'machine learning', 'deep learning', 'data analysis', 'statistics', 'data science',
                'pandas', 'numpy', 'scikit-learn', 'tensorflow', 'pytorch', 'keras', 'matplotlib',
                'seaborn', 'spacy', 'nltk', 'nlp'
            ],
            'cloud_devops': [
                'aws', 'azure', 'gcp', 'google cloud', 'docker', 'kubernetes', 'jenkins',
                'terraform', 'ansible', 'ci/cd', 'gitlab', 'github', 'bitbucket', 'devops',
                'heroku', 'aws lambda'
            ],
            'tools': [
                'git', 'github', 'gitlab', 'jira', 'confluence', 'slack', 'docker',
                'postman', 'vim', 'vscode', 'visual studio', 'intellij', 'eclipse',
                'tableau', 'power bi', 'excel', 'powerpoint', 'word', 'photoshop'
            ],
            'soft_skills': [
                'communication', 'leadership', 'teamwork', 'problem solving', 'analytical',
                'project management', 'agile', 'scrum', 'kanban', 'planning', 'mentoring',
                'presentation', 'negotiation'
            ]
        }
        
        # Education patterns
        self.education_patterns = {
            'degree_types': ['bachelor', 'master', 'phd', 'doctorate', 'associate', 'diploma'],
            'fields': ['computer science', 'engineering', 'business', 'mathematics', 'science', 'arts']
        }
    
    def extract_information(self, file_content: Any):
        """
        Extract information from resume text or file object
        """
        try:
            # Handle both file objects and raw strings
            if hasattr(file_content, 'read'):
                content = file_content.read()
                if isinstance(content, bytes):
                    content = content.decode('utf-8', errors='ignore')
            else:
                content = str(file_content)
            
            extracted_data = {
                'skills': self._extract_skills(content),
                'education': self._extract_education(content),
                'experience': self._extract_experience(content),
                'contact_info': self._extract_contact_info(content),
                'summary': self._extract_summary(content),
                'raw_text_preview': content[:1000] # Safe preview
            }
            
            return {
                'status': 'success',
                'data': extracted_data,
                'message': 'Resume analyzed successfully'
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'data': {},
                'message': f'Error analyzing resume: {str(e)}'
            }
    
    def _extract_skills(self, text: str) -> List[str]:
        """Extract skills using both section-based and global pattern matching"""
        text_lower = text.lower()
        found_skills = []

        # 1. Try to find skills in specific sections first
        found_skills.extend(self._extract_skills_from_sections(text))
        
        # 2. Pattern match against the entire text
        for category, skills in self.skill_patterns.items():
            for skill in skills:
                # \b ensures we don't match 'Java' inside 'Javascript'
                pattern = r'\b' + re.escape(skill) + r'\b'
                if re.search(pattern, text_lower):
                    found_skills.append(skill.title())
        
        # Cleanup: Remove duplicates and normalize
        return list(set([s.strip().title() for s in found_skills if s.strip()]))

    def _extract_skills_from_sections(self, text: str) -> List[str]:
        headings = {'skills', 'technical skills', 'technologies', 'tools', 'expertise', 'competencies'}
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        collected = []

        i = 0
        while i < len(lines):
            line_clean = lines[i].lower().strip(':- ')
            if line_clean in headings:
                i += 1
                while i < len(lines):
                    next_line = lines[i].strip()
                    # If we hit another heading, stop
                    if next_line.lower().strip(':- ') in headings:
                        break
                    
                    # Split by common delimiters
                    parts = re.split(r'[•|,;/]+', next_line)
                    for part in parts:
                        cleaned = part.strip()
                        if cleaned and len(cleaned) < 30: # Avoid capturing long sentences
                            collected.append(cleaned)
                    i += 1
                continue
            i += 1
        return collected
    
    def _extract_education(self, text: str) -> Dict[str, Any]:
        text_lower = text.lower()
        education_info = {'degree': None, 'field': None, 'year': None}
        
        for degree in self.education_patterns['degree_types']:
            if degree in text_lower:
                education_info['degree'] = degree.title()
                break
        
        for field in self.education_patterns['fields']:
            if field in text_lower:
                education_info['field'] = field.title()
                break
        
        years = re.findall(r'20\d{2}|19\d{2}', text)
        if years:
            education_info['year'] = years[-1] 
        
        return education_info
    
    def _extract_experience(self, text: str) -> List[Dict[str, Any]]:
        experience_keywords = ['experience', 'work', 'employment', 'position', 'role']
        experiences = []
        total_years = self._estimate_years_from_dates(text)

        if any(keyword in text.lower() for keyword in experience_keywords):
            experiences.append({
                'position': 'Professional Experience Found',
                'years': total_years,
                'duration_desc': f'{total_years} years' if total_years > 0 else 'Recent Experience'
            })
        return experiences

    def _estimate_years_from_dates(self, text: str) -> float:
        current_year = datetime.now(timezone.utc).year
        # Matches 2018-2022 or 2019 - Present
        year_ranges = re.findall(r'((?:19|20)\d{2})\s*[-–]\s*((?:19|20)\d{2}|present|current|now)', text.lower())
        
        total = 0.0
        for start_str, end_str in year_ranges:
            try:
                start = int(start_str)
                end = current_year if end_str in ('present', 'current', 'now') else int(end_str)
                if end >= start:
                    total += max(0.5, float(end - start))
            except ValueError:
                continue
        return total
    
    def _extract_contact_info(self, text: str) -> Dict[str, Any]:
        contact_info = {'email': None, 'phone': None}
        
        email_match = re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
        if email_match:
            contact_info['email'] = email_match.group(0)
        
        phone_match = re.search(r'[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}', text)
        if phone_match:
            contact_info['phone'] = phone_match.group(0)
            
        return contact_info
    
    def _extract_summary(self, text: str) -> str:
        # Take the first non-empty line as a candidate for a summary/title
        lines = [l.strip() for l in text.split('\n') if l.strip()]
        if not lines:
            return "No text content found."
        
        summary = lines[0]
        if len(summary) > 200:
            summary = summary[:197] + "..."
        return summary

    def analyze_skills_gap(self, user_skills: List[str], job_requirements: List[str]) -> Dict[str, Any]:
        u_skills = set(s.lower() for s in user_skills)
        j_reqs = set(s.lower() for s in job_requirements)
        
        matched = list(u_skills.intersection(j_reqs))
        missing = list(j_reqs.difference(u_skills))
        
        percentage = (len(matched) / len(j_reqs) * 100) if j_reqs else 0
        
        return {
            'matching_skills': [s.title() for s in matched],
            'missing_skills': [s.title() for s in missing],
            'match_percentage': round(percentage, 1)
        }