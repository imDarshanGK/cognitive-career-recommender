"""
Simplified NLP-based Resume Analyzer for Cognitive Career Recommendation System
"""

import re
from typing import Dict, List, Any, Optional

class ResumeAnalyzer:
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
    
    def extract_information(self, file):
        """
        Extract information from uploaded resume file
        
        Args:
            file: Uploaded file object
            
        Returns:
            Dict containing extracted resume information
        """
        try:
            # Read file content
            if hasattr(file, 'read'):
                content = file.read()
                if isinstance(content, bytes):
                    content = content.decode('utf-8', errors='ignore')
            else:
                content = str(file)
            
            # Extract information
            extracted_data = {
                'skills': self._extract_skills(content),
                'education': self._extract_education(content),
                'experience': self._extract_experience(content),
                'contact_info': self._extract_contact_info(content),
                'summary': self._extract_summary(content)
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
        """Extract skills from resume text using word boundary matching"""
        text_lower = text.lower()
        found_skills = []
        
        for category, skills in self.skill_patterns.items():
            for skill in skills:
                # Use word boundaries to ensure exact skill matching
                # Convert skill to regex pattern with word boundaries
                import re as regex_module
                pattern = r'\b' + regex_module.escape(skill) + r'\b'
                if regex_module.search(pattern, text_lower):
                    found_skills.append(skill.title())
        
        return list(set(found_skills))  # Remove duplicates
    
    def _extract_education(self, text: str) -> Dict[str, Any]:
        """Extract education information from resume text"""
        text_lower = text.lower()
        
        education_info = {
            'degree': None,
            'field': None,
            'institution': None,
            'year': None
        }
        
        # Find degree types
        for degree in self.education_patterns['degree_types']:
            if degree in text_lower:
                education_info['degree'] = degree.title()
                break
        
        # Find fields of study
        for field in self.education_patterns['fields']:
            if field in text_lower:
                education_info['field'] = field.title()
                break
        
        # Extract year (basic regex for 4-digit years)
        year_pattern = r'20\d{2}|19\d{2}'
        years = re.findall(year_pattern, text)
        if years:
            education_info['year'] = years[-1]  # Take the most recent year
        
        return education_info
    
    def _extract_experience(self, text: str) -> List[Dict[str, Any]]:
        """Extract work experience from resume text"""
        # This is a simplified version - in reality would be much more complex
        experience_keywords = ['experience', 'work', 'employment', 'position', 'role']
        
        experiences = []
        
        # Look for experience sections
        if any(keyword in text.lower() for keyword in experience_keywords):
            experiences.append({
                'position': 'Professional Experience Found',
                'company': 'Various Companies',
                'duration': 'Multiple Years',
                'description': 'Professional experience detected in resume'
            })
        
        return experiences
    
    def _extract_contact_info(self, text: str) -> Dict[str, Any]:
        """Extract contact information from resume text"""
        contact_info = {
            'email': None,
            'phone': None,
            'linkedin': None
        }
        
        # Extract email
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, text)
        if emails:
            contact_info['email'] = emails[0]
        
        # Extract phone number (basic pattern)
        phone_pattern = r'[\+]?[1-9]?[0-9]{7,12}'
        phones = re.findall(phone_pattern, text)
        if phones:
            contact_info['phone'] = phones[0]
        
        # Check for LinkedIn
        if 'linkedin' in text.lower():
            contact_info['linkedin'] = 'LinkedIn profile found'
        
        return contact_info
    
    def _extract_summary(self, text: str) -> str:
        """Extract or create a summary of the resume"""
        # Get first few sentences as summary
        sentences = text.split('.')[:3]
        summary = '. '.join(sentences).strip()
        
        if len(summary) > 500:
            summary = summary[:500] + '...'
        
        return summary or "Professional resume with relevant experience and skills."

    def analyze_skills_gap(self, user_skills: List[str], job_requirements: List[str]) -> Dict[str, Any]:
        """
        Analyze skills gap between user skills and job requirements
        
        Args:
            user_skills: List of user's current skills
            job_requirements: List of required skills for target job
            
        Returns:
            Skills gap analysis
        """
        user_skills_lower = [skill.lower() for skill in user_skills]
        job_requirements_lower = [skill.lower() for skill in job_requirements]
        
        matching_skills = [skill for skill in job_requirements_lower if skill in user_skills_lower]
        missing_skills = [skill for skill in job_requirements_lower if skill not in user_skills_lower]
        
        return {
            'matching_skills': matching_skills,
            'missing_skills': missing_skills,
            'match_percentage': len(matching_skills) / len(job_requirements) * 100 if job_requirements else 0,
            'recommendations': self._generate_skill_recommendations(missing_skills)
        }
    
    def _generate_skill_recommendations(self, missing_skills: List[str]) -> List[str]:
        """Generate learning recommendations for missing skills"""
        recommendations = []
        
        for skill in missing_skills:
            if skill in ['python', 'java', 'javascript']:
                recommendations.append(f"Consider taking an online course in {skill} programming")
            elif skill in ['machine learning', 'data analysis']:
                recommendations.append(f"Explore {skill} through online platforms like Coursera or edX")
            else:
                recommendations.append(f"Gain experience in {skill} through practice projects")
        
        return recommendations