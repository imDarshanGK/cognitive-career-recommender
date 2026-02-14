"""
Skill Matching Engine
Core AI Logic for matching user skills with job requirements
"""

import numpy as np

# Optional sklearn imports
try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False

from models import db, User, UserSkill, Job, JobSkill

class SkillMatcher:
    """
    Match user skills with job requirements
    Uses TF-IDF and cosine similarity
    """
    
    @staticmethod
    def calculate_match_score(user_id, job_id):
        """
        Calculate match score between user and job (0-100)
        Returns: score
        """
        # Get user skills
        user_skills = UserSkill.query.filter_by(user_id=user_id).all()
        user_skill_names = {s.skill_name.lower(): s.skill_level for s in user_skills}
        
        # Get job skills
        job_skills = JobSkill.query.filter_by(job_id=job_id).all()
        job_skill_names = {s.skill_name.lower(): s.required_level for s in job_skills}
        
        if not job_skill_names:
            return 0
        
        # Calculate matches
        matched = 0
        mandatory_found = 0
        mandatory_total = 0
        
        for job_skill, required_level in job_skill_names.items():
            if job_skill in user_skill_names:
                matched += 1
                if job_skill in {s.skill_name.lower() for s in job_skills if s.is_mandatory}:
                    mandatory_found += 1
        
        for skill in job_skills:
            if skill.is_mandatory:
                mandatory_total += 1
        
        # Calculate base score
        if len(job_skill_names) > 0:
            match_percentage = (matched / len(job_skill_names)) * 100
        else:
            match_percentage = 0
        
        # Mandatory skills weighting (50% of score)
        if mandatory_total > 0:
            mandatory_score = (mandatory_found / mandatory_total) * 50
        else:
            mandatory_score = 50  # All skills are covered
        
        # Total score: mandatory (50%) + optional (50%)
        total_score = (match_percentage * 0.5) + mandatory_score
        
        # Cap at 100
        return min(total_score, 100)
    
    @staticmethod
    def get_matched_skills(user_id, job_id):
        """Get skills that user has and job requires"""
        user_skills = {s.skill_name.lower(): s for s in UserSkill.query.filter_by(user_id=user_id).all()}
        job_skills = {s.skill_name.lower(): s for s in JobSkill.query.filter_by(job_id=job_id).all()}
        
        matched = {}
        for skill_name in job_skills:
            if skill_name in user_skills:
                matched[skill_name] = {
                    'user_level': user_skills[skill_name].skill_level,
                    'required_level': job_skills[skill_name].required_level
                }
        
        return matched
    
    @staticmethod
    def get_missing_skills(user_id, job_id):
        """Get skills that job requires but user doesn't have"""
        user_skills = {s.skill_name.lower() for s in UserSkill.query.filter_by(user_id=user_id).all()}
        job_skills = JobSkill.query.filter_by(job_id=job_id).all()
        
        missing = {}
        for skill in job_skills:
            if skill.skill_name.lower() not in user_skills:
                missing[skill.skill_name] = {
                    'required_level': skill.required_level,
                    'is_mandatory': skill.is_mandatory
                }
        
        return missing
    
    @staticmethod
    def get_all_recommendations(user_id, limit=10):
        """
        Get all job recommendations for a user, sorted by score
        Returns: list of (job, score) tuples
        """
        jobs = Job.query.all()
        recommendations = []
        
        for job in jobs:
            score = SkillMatcher.calculate_match_score(user_id, job.id)
            if score > 0:
                recommendations.append((job, score))
        
        # Sort by score descending
        recommendations.sort(key=lambda x: x[1], reverse=True)
        
        return recommendations[:limit]
