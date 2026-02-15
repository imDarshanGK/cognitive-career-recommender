"""
Skill Extractor
Extracts skills from resume text using NLP
"""

import re

class SkillExtractor:
    """
    Extract skills from resume text
    Uses pattern matching and skill database
    """
    
    # Comprehensive skill database
    SKILLS_DB = {
        'Programming Languages': [
            'Python', 'Java', 'JavaScript', 'C++', 'C', 'C#', 'Ruby', 'PHP', 'Go', 'Rust',
            'TypeScript', 'Swift', 'Kotlin', 'R', 'MATLAB', 'Scala', 'Perl', 'Shell',
            'Bash', 'SQL', 'HTML', 'CSS', 'XML', 'JSON'
        ],
        'Web Development': [
            'React', 'Angular', 'Vue.js', 'Node.js', 'Express', 'Django', 'Flask',
            'Spring', 'ASP.NET', 'FastAPI', 'Bootstrap', 'Tailwind CSS', 'Material Design',
            'REST API', 'GraphQL', 'WebSocket', 'AJAX'
        ],
        'Data Science & ML': [
            'Machine Learning', 'Deep Learning', 'TensorFlow', 'PyTorch', 'Keras',
            'Scikit-learn', 'Pandas', 'NumPy', 'Matplotlib', 'Seaborn', 'Data Analysis',
            'Data Visualization', 'NLP', 'Computer Vision', 'Statistical Analysis',
            'Regression', 'Classification', 'Clustering', 'CNN', 'RNN', 'LSTM', 'Neural Networks'
        ],
        'Databases': [
            'MySQL', 'PostgreSQL', 'MongoDB', 'Redis', 'Cassandra', 'Oracle', 'SQLite',
            'Firebase', 'AWS DynamoDB', 'Elasticsearch', 'Database Design', 'SQL Optimization'
        ],
        'DevOps & Cloud': [
            'Docker', 'Kubernetes', 'AWS', 'Azure', 'Google Cloud', 'CI/CD', 'Jenkins',
            'GitLab CI', 'GitHub Actions', 'Terraform', 'Ansible', 'CloudFormation',
            'Linux', 'Unix', 'AWS EC2', 'AWS S3', 'Lambda'
        ],
        'Tools & Platforms': [
            'Git', 'GitHub', 'GitLab', 'Bitbucket', 'Jira', 'Slack', 'Confluence',
            'Visual Studio Code', 'IntelliJ', 'Sublime Text', 'Jupyter', 'Anaconda'
        ],
        'Soft Skills': [
            'Team Leadership', 'Project Management', 'Communication', 'Problem Solving',
            'Analytical Thinking', 'Critical Thinking', 'Time Management', 'Collaboration',
            'Attention to Detail', 'Adaptability', 'Creativity', 'Documentation'
        ],
        'Methodologies': [
            'Agile', 'Scrum', 'Kanban', 'Waterfall', 'Test-Driven Development', 'TDD',
            'Continuous Integration', 'DevOps', 'Microservices'
        ]
    }
    
    def __init__(self):
        # Flatten skill database
        self.all_skills = set()
        for category, skills in self.SKILLS_DB.items():
            self.all_skills.update([s.lower() for s in skills])
    
    def extract_skills(self, text):
        """
        Extract skills from resume text
        Returns: list of skills found
        """
        if not text:
            return []
        
        text_lower = text.lower()
        found_skills = []
        
        # Match skills against database
        for skill in self.all_skills:
            # Use word boundary matching to avoid partial matches
            pattern = r'\b' + re.escape(skill) + r'\b'
            if re.search(pattern, text_lower, re.IGNORECASE):
                # Find original case from database
                for category, skills in self.SKILLS_DB.items():
                    for original_skill in skills:
                        if original_skill.lower() == skill:
                            found_skills.append(original_skill)
                            break
        
        # Remove duplicates and return
        return list(set(found_skills))
