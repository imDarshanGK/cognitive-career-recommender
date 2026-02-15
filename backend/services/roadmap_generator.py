"""
Career Roadmap Generator
Generates learning paths to bridge skill gaps
"""

import json

class RoadmapGenerator:
    """
    Generate personalized learning roadmaps
    Based on skill gaps to reach career goals
    """
    
    # Learning path templates for different domains
    LEARNING_PATHS = {
        'AI': [
            {
                'step': 1,
                'skill': 'Mathematics Foundations',
                'duration': '4-6 weeks',
                'resources': 'Linear Algebra, Calculus, Probability & Statistics',
                'difficulty': 'Medium'
            },
            {
                'step': 2,
                'skill': 'Machine Learning Fundamentals',
                'duration': '8-10 weeks',
                'resources': 'Coursera ML Course, scikit-learn tutorials',
                'difficulty': 'Medium'
            },
            {
                'step': 3,
                'skill': 'Deep Learning',
                'duration': '10-12 weeks',
                'resources': 'TensorFlow, PyTorch courses, Papers',
                'difficulty': 'Hard'
            },
            {
                'step': 4,
                'skill': 'Advanced Topics',
                'duration': '12+ weeks',
                'resources': 'NLP, Computer Vision, RL, Research Papers',
                'difficulty': 'Hard'
            },
            {
                'step': 5,
                'skill': 'Portfolio Projects',
                'duration': 'Ongoing',
                'resources': 'Kaggle, GitHub, Personal Projects',
                'difficulty': 'Medium'
            }
        ],
        'Data Science': [
            {
                'step': 1,
                'skill': 'Data Analysis Fundamentals',
                'duration': '4-6 weeks',
                'resources': 'Pandas, NumPy, pandas documentation',
                'difficulty': 'Easy'
            },
            {
                'step': 2,
                'skill': 'Statistics & Probability',
                'duration': '6-8 weeks',
                'resources': 'Khan Academy, Coursera Statistics',
                'difficulty': 'Medium'
            },
            {
                'step': 3,
                'skill': 'Data Visualization',
                'duration': '4-5 weeks',
                'resources': 'Matplotlib, Seaborn, Tableau tutorials',
                'difficulty': 'Easy'
            },
            {
                'step': 4,
                'skill': 'Machine Learning',
                'duration': '8-10 weeks',
                'resources': 'Scikit-learn, ML courses',
                'difficulty': 'Medium'
            },
            {
                'step': 5,
                'skill': 'Advanced Analytics',
                'duration': 'Ongoing',
                'resources': 'Time series, Causal inference, A/B testing',
                'difficulty': 'Hard'
            }
        ],
        'Web': [
            {
                'step': 1,
                'skill': 'Frontend Fundamentals',
                'duration': '4-6 weeks',
                'resources': 'HTML, CSS, JavaScript basics',
                'difficulty': 'Easy'
            },
            {
                'step': 2,
                'skill': 'React Basics',
                'duration': '6-8 weeks',
                'resources': 'React official tutorial, Scrimba courses',
                'difficulty': 'Medium'
            },
            {
                'step': 3,
                'skill': 'Backend Development',
                'duration': '8-10 weeks',
                'resources': 'Node.js, Express, Python Flask/Django',
                'difficulty': 'Medium'
            },
            {
                'step': 4,
                'skill': 'Databases',
                'duration': '4-6 weeks',
                'resources': 'SQL, MongoDB, database design',
                'difficulty': 'Medium'
            },
            {
                'step': 5,
                'skill': 'Full Stack Projects',
                'duration': 'Ongoing',
                'resources': 'Build real applications, GitHub portfolio',
                'difficulty': 'Medium'
            }
        ],
        'Cloud': [
            {
                'step': 1,
                'skill': 'Linux Fundamentals',
                'duration': '4-6 weeks',
                'resources': 'Linux command line, Linux Academy',
                'difficulty': 'Easy'
            },
            {
                'step': 2,
                'skill': 'AWS Basics',
                'duration': '6-8 weeks',
                'resources': 'AWS Free Tier, A Cloud Guru courses',
                'difficulty': 'Medium'
            },
            {
                'step': 3,
                'skill': 'Docker & Containerization',
                'duration': '4-6 weeks',
                'resources': 'Docker documentation, Hands-on labs',
                'difficulty': 'Medium'
            },
            {
                'step': 4,
                'skill': 'Kubernetes Orchestration',
                'duration': '6-8 weeks',
                'resources': 'Kubernetes docs, KodeKloud courses',
                'difficulty': 'Hard'
            },
            {
                'step': 5,
                'skill': 'CI/CD & DevOps',
                'duration': '6-8 weeks',
                'resources': 'Jenkins, GitLab CI, Terraform',
                'difficulty': 'Hard'
            }
        ]
    }
    
    @staticmethod
    def generate_roadmap(job_domain, missing_skills):
        """
        Generate learning roadmap based on job domain and missing skills
        Returns: list of learning steps
        """
        base_path = RoadmapGenerator.LEARNING_PATHS.get(job_domain, [])
        
        if not base_path:
            return RoadmapGenerator._create_custom_roadmap(missing_skills)
        
        # Filter roadmap based on missing skills
        filtered_path = []
        missing_skills_lower = {s.lower() for s in missing_skills.keys()}
        
        for step in base_path:
            # Include step if it contains any missing skill
            if any(skill_word in step['skill'].lower() for skill_word in missing_skills_lower) or step['step'] <= 2:
                filtered_path.append(step)
        
        return filtered_path if filtered_path else base_path
    
    @staticmethod
    def _create_custom_roadmap(missing_skills):
        """Create custom roadmap for missing skills"""
        roadmap = []
        
        for idx, (skill, details) in enumerate(missing_skills.items(), 1):
            roadmap.append({
                'step': idx,
                'skill': skill,
                'duration': '4-8 weeks',
                'resources': f'{skill} tutorials, courses, documentation',
                'difficulty': 'Beginner' if details['required_level'] == 'beginner' else 'Medium',
                'is_mandatory': details['is_mandatory']
            })
        
        return roadmap
