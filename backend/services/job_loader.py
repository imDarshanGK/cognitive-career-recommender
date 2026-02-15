"""
Job Dataset Loader
Loads and initializes job data from public datasets
"""

import json
from models import db, Job, JobSkill

class JobDatasetLoader:
    """
    Load realistic job data
    Uses public datasets like O*NET, Kaggle job datasets
    """
    
    # Sample job dataset (can be expanded with real data)
    JOB_DATA = [
        {
            'job_title': 'Machine Learning Engineer',
            'description': 'Develop and deploy ML models for production systems. Work on model optimization, scaling, and real-world applications.',
            'domain': 'AI',
            'experience_level': 'intermediate',
            'average_salary': '$120,000 - $180,000',
            'job_market_demand': 9.5,
            'skills': [
                {'name': 'Python', 'required_level': 'expert', 'is_mandatory': True},
                {'name': 'Machine Learning', 'required_level': 'expert', 'is_mandatory': True},
                {'name': 'Deep Learning', 'required_level': 'intermediate', 'is_mandatory': False},
                {'name': 'TensorFlow', 'required_level': 'intermediate', 'is_mandatory': False},
                {'name': 'PyTorch', 'required_level': 'intermediate', 'is_mandatory': False},
                {'name': 'SQL', 'required_level': 'intermediate', 'is_mandatory': True},
                {'name': 'Data Analysis', 'required_level': 'expert', 'is_mandatory': True},
                {'name': 'Statistics', 'required_level': 'intermediate', 'is_mandatory': True},
                {'name': 'AWS', 'required_level': 'intermediate', 'is_mandatory': False},
                {'name': 'Docker', 'required_level': 'intermediate', 'is_mandatory': False},
            ]
        },
        {
            'job_title': 'Data Scientist',
            'description': 'Analyze complex datasets to drive business decisions. Create predictive models and data visualizations.',
            'domain': 'Data Science',
            'experience_level': 'intermediate',
            'average_salary': '$100,000 - $160,000',
            'job_market_demand': 9.0,
            'skills': [
                {'name': 'Python', 'required_level': 'expert', 'is_mandatory': True},
                {'name': 'Data Analysis', 'required_level': 'expert', 'is_mandatory': True},
                {'name': 'Statistics', 'required_level': 'expert', 'is_mandatory': True},
                {'name': 'Machine Learning', 'required_level': 'intermediate', 'is_mandatory': True},
                {'name': 'SQL', 'required_level': 'expert', 'is_mandatory': True},
                {'name': 'Pandas', 'required_level': 'intermediate', 'is_mandatory': False},
                {'name': 'Matplotlib', 'required_level': 'intermediate', 'is_mandatory': False},
                {'name': 'R', 'required_level': 'beginner', 'is_mandatory': False},
            ]
        },
        {
            'job_title': 'Full Stack Developer',
            'description': 'Build end-to-end web applications. Work on both frontend and backend development.',
            'domain': 'Web',
            'experience_level': 'intermediate',
            'average_salary': '$90,000 - $150,000',
            'job_market_demand': 9.2,
            'skills': [
                {'name': 'JavaScript', 'required_level': 'expert', 'is_mandatory': True},
                {'name': 'React', 'required_level': 'intermediate', 'is_mandatory': True},
                {'name': 'Node.js', 'required_level': 'intermediate', 'is_mandatory': True},
                {'name': 'HTML', 'required_level': 'expert', 'is_mandatory': True},
                {'name': 'CSS', 'required_level': 'intermediate', 'is_mandatory': True},
                {'name': 'SQL', 'required_level': 'intermediate', 'is_mandatory': True},
                {'name': 'MongoDB', 'required_level': 'intermediate', 'is_mandatory': False},
                {'name': 'REST API', 'required_level': 'intermediate', 'is_mandatory': True},
                {'name': 'Git', 'required_level': 'intermediate', 'is_mandatory': True},
            ]
        },
        {
            'job_title': 'Frontend Developer',
            'description': 'Create responsive and interactive user interfaces. Focus on user experience and web standards.',
            'domain': 'Web',
            'experience_level': 'intermediate',
            'average_salary': '$80,000 - $140,000',
            'job_market_demand': 8.8,
            'skills': [
                {'name': 'JavaScript', 'required_level': 'expert', 'is_mandatory': True},
                {'name': 'React', 'required_level': 'expert', 'is_mandatory': True},
                {'name': 'HTML', 'required_level': 'expert', 'is_mandatory': True},
                {'name': 'CSS', 'required_level': 'expert', 'is_mandatory': True},
                {'name': 'TypeScript', 'required_level': 'intermediate', 'is_mandatory': False},
                {'name': 'Vue.js', 'required_level': 'beginner', 'is_mandatory': False},
                {'name': 'REST API', 'required_level': 'intermediate', 'is_mandatory': True},
                {'name': 'Git', 'required_level': 'intermediate', 'is_mandatory': True},
            ]
        },
        {
            'job_title': 'Backend Developer',
            'description': 'Build scalable server-side applications. Manage databases and APIs.',
            'domain': 'Web',
            'experience_level': 'intermediate',
            'average_salary': '$100,000 - $160,000',
            'job_market_demand': 8.9,
            'skills': [
                {'name': 'Python', 'required_level': 'expert', 'is_mandatory': True},
                {'name': 'Node.js', 'required_level': 'intermediate', 'is_mandatory': True},
                {'name': 'SQL', 'required_level': 'expert', 'is_mandatory': True},
                {'name': 'REST API', 'required_level': 'expert', 'is_mandatory': True},
                {'name': 'MongoDB', 'required_level': 'intermediate', 'is_mandatory': False},
                {'name': 'Docker', 'required_level': 'intermediate', 'is_mandatory': False},
                {'name': 'AWS', 'required_level': 'intermediate', 'is_mandatory': False},
                {'name': 'Git', 'required_level': 'intermediate', 'is_mandatory': True},
            ]
        },
        {
            'job_title': 'DevOps Engineer',
            'description': 'Manage cloud infrastructure, deployment pipelines, and system reliability.',
            'domain': 'Cloud',
            'experience_level': 'intermediate',
            'average_salary': '$110,000 - $170,000',
            'job_market_demand': 8.7,
            'skills': [
                {'name': 'Docker', 'required_level': 'expert', 'is_mandatory': True},
                {'name': 'Kubernetes', 'required_level': 'intermediate', 'is_mandatory': True},
                {'name': 'AWS', 'required_level': 'expert', 'is_mandatory': True},
                {'name': 'Linux', 'required_level': 'expert', 'is_mandatory': True},
                {'name': 'Python', 'required_level': 'intermediate', 'is_mandatory': False},
                {'name': 'Bash', 'required_level': 'intermediate', 'is_mandatory': True},
                {'name': 'Git', 'required_level': 'intermediate', 'is_mandatory': True},
                {'name': 'CI/CD', 'required_level': 'intermediate', 'is_mandatory': True},
            ]
        },
        {
            'job_title': 'Solutions Architect',
            'description': 'Design scalable technical solutions. Bridge between business requirements and technical implementation.',
            'domain': 'Enterprise',
            'experience_level': 'senior',
            'average_salary': '$130,000 - $200,000',
            'job_market_demand': 7.9,
            'skills': [
                {'name': 'Python', 'required_level': 'intermediate', 'is_mandatory': False},
                {'name': 'AWS', 'required_level': 'expert', 'is_mandatory': True},
                {'name': 'Azure', 'required_level': 'intermediate', 'is_mandatory': False},
                {'name': 'System Design', 'required_level': 'expert', 'is_mandatory': True},
                {'name': 'Microservices', 'required_level': 'expert', 'is_mandatory': True},
                {'name': 'Docker', 'required_level': 'intermediate', 'is_mandatory': True},
                {'name': 'Kubernetes', 'required_level': 'intermediate', 'is_mandatory': False},
            ]
        },
        {
            'job_title': 'Cloud Engineer',
            'description': 'Manage cloud platforms and services. Optimize cloud infrastructure and costs.',
            'domain': 'Cloud',
            'experience_level': 'intermediate',
            'average_salary': '$105,000 - $165,000',
            'job_market_demand': 8.5,
            'skills': [
                {'name': 'AWS', 'required_level': 'expert', 'is_mandatory': True},
                {'name': 'Python', 'required_level': 'intermediate', 'is_mandatory': False},
                {'name': 'Linux', 'required_level': 'intermediate', 'is_mandatory': True},
                {'name': 'Docker', 'required_level': 'intermediate', 'is_mandatory': False},
                {'name': 'Terraform', 'required_level': 'intermediate', 'is_mandatory': False},
                {'name': 'Bash', 'required_level': 'intermediate', 'is_mandatory': True},
            ]
        },
        {
            'job_title': 'AI Research Engineer',
            'description': 'Research and develop cutting-edge AI/ML models. Publish papers and advance the field.',
            'domain': 'AI',
            'experience_level': 'senior',
            'average_salary': '$130,000 - $200,000',
            'job_market_demand': 8.2,
            'skills': [
                {'name': 'Python', 'required_level': 'expert', 'is_mandatory': True},
                {'name': 'Machine Learning', 'required_level': 'expert', 'is_mandatory': True},
                {'name': 'Deep Learning', 'required_level': 'expert', 'is_mandatory': True},
                {'name': 'TensorFlow', 'required_level': 'intermediate', 'is_mandatory': False},
                {'name': 'PyTorch', 'required_level': 'expert', 'is_mandatory': True},
                {'name': 'NLP', 'required_level': 'intermediate', 'is_mandatory': False},
                {'name': 'Computer Vision', 'required_level': 'intermediate', 'is_mandatory': False},
                {'name': 'Statistics', 'required_level': 'expert', 'is_mandatory': True},
            ]
        }
    ]
    
    @staticmethod
    def load_job_dataset():
        """
        Load job dataset into database
        Call this once during initialization
        """
        # Check if jobs already exist
        existing_count = Job.query.count()
        if existing_count > 0:
            print(f"Jobs already loaded: {existing_count} jobs found")
            return
        
        try:
            for job_data in JobDatasetLoader.JOB_DATA:
                job = Job(
                    job_title=job_data['job_title'],
                    description=job_data['description'],
                    domain=job_data['domain'],
                    experience_level=job_data['experience_level'],
                    average_salary=job_data['average_salary'],
                    job_market_demand=job_data['job_market_demand']
                )
                db.session.add(job)
                db.session.flush()  # Get job ID
                
                # Add skills
                for skill_data in job_data['skills']:
                    skill = JobSkill(
                        job_id=job.id,
                        skill_name=skill_data['name'],
                        required_level=skill_data['required_level'],
                        is_mandatory=skill_data['is_mandatory']
                    )
                    db.session.add(skill)
            
            db.session.commit()
            print(f"Loaded {len(JobDatasetLoader.JOB_DATA)} jobs successfully")
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Error loading jobs: {str(e)}")
            return False
