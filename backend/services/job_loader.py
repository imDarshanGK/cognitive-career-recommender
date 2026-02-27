"""
Job Dataset Loader
Standardizes and seeds the database with career-specific skill taxonomies.
"""

import logging
from models import db, Job, JobSkill

logger = logging.getLogger(__name__)

class JobDatasetLoader:
    """
    Handles the initial ingestion of career data.
    Maps complex job roles to granular skill requirements.
    """
    
    # ... (JOB_DATA remains as you defined it)

    @staticmethod
    def load_job_dataset():
        """
        Populates the database. Designed to be called during app factory initialization.
        """
        try:
            # 1. Idempotency Check
            if Job.query.first():
                logger.info("Job dataset already initialized. Skipping seeding.")
                return True
            
            # 2. Bulk Insertion Strategy
            for job_data in JobDatasetLoader.JOB_DATA:
                new_job = Job(
                    job_title=job_data['job_title'],
                    description=job_data['description'],
                    domain=job_data['domain'],
                    experience_level=job_data['experience_level'].lower(),
                    average_salary=job_data['average_salary'],
                    job_market_demand=job_data['job_market_demand']
                )
                db.session.add(new_job)
                db.session.flush()  # Populates new_job.id for foreign key use
                
                # 3. Normalized Skill Mapping
                skill_objects = []
                for s in job_data['skills']:
                    skill_objects.append(JobSkill(
                        job_id=new_job.id,
                        skill_name=s['name'].strip().lower(), # Crucial for matching
                        required_level=s['required_level'].lower(),
                        is_mandatory=s.get('is_mandatory', False)
                    ))
                
                db.session.add_all(skill_objects)
            
            db.session.commit()
            logger.info(f"Successfully seeded {len(JobDatasetLoader.JOB_DATA)} career roles.")
            return True

        except Exception as e:
            db.session.rollback()
            logger.error(f"Critical failure during job seeding: {str(e)}")
            return False