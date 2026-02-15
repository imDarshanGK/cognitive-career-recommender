"""
Profile Service
Manages user profile creation and updates
"""

from models import db, UserProfile, UserSkill

class ProfileService:
    @staticmethod
    def create_profile(user_id, education_level=None, branch=None, experience_years=0, preferred_domains=None):
        """Create user profile"""
        profile = UserProfile.query.filter_by(user_id=user_id).first()
        
        if profile:
            # Update existing profile
            profile.education_level = education_level or profile.education_level
            profile.branch = branch or profile.branch
            profile.experience_years = experience_years or profile.experience_years
            profile.preferred_domains = preferred_domains or profile.preferred_domains
        else:
            # Create new profile
            profile = UserProfile(
                user_id=user_id,
                education_level=education_level,
                branch=branch,
                experience_years=experience_years,
                preferred_domains=preferred_domains
            )
            db.session.add(profile)
        
        # Calculate completeness
        ProfileService.calculate_completeness(profile)
        
        try:
            db.session.commit()
            return profile, None
        except Exception as e:
            db.session.rollback()
            return None, str(e)
    
    @staticmethod
    def add_skill(user_id, skill_name, skill_level='intermediate', years_experience=0):
        """Add or update user skill"""
        skill = UserSkill.query.filter_by(user_id=user_id, skill_name=skill_name).first()
        
        if skill:
            skill.skill_level = skill_level
            skill.years_experience = years_experience
        else:
            skill = UserSkill(
                user_id=user_id,
                skill_name=skill_name,
                skill_level=skill_level,
                years_experience=years_experience
            )
            db.session.add(skill)
        
        try:
            db.session.commit()
            return skill, None
        except Exception as e:
            db.session.rollback()
            return None, str(e)
    
    @staticmethod
    def get_user_skills(user_id):
        """Get all skills for a user"""
        skills = UserSkill.query.filter_by(user_id=user_id).all()
        return [skill.to_dict() for skill in skills]
    
    @staticmethod
    def calculate_completeness(profile):
        """Calculate profile completeness percentage"""
        completeness = 0
        
        if profile.education_level:
            completeness += 25
        if profile.branch:
            completeness += 25
        if profile.experience_years > 0:
            completeness += 25
        if profile.preferred_domains:
            completeness += 25
        
        profile.profile_completeness = completeness
        return completeness
    
    @staticmethod
    def get_profile(user_id):
        """Get user profile"""
        return UserProfile.query.filter_by(user_id=user_id).first()
