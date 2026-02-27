"""
Profile Service
Manages user profile creation, skill synchronization, and metadata updates.
"""

from models import db, UserProfile, UserSkill
import logging

logger = logging.getLogger(__name__)

class ProfileService:
    @staticmethod
    def create_or_update_profile(user_id, **kwargs):
        """
        Maintains a single user profile using keyword arguments for flexibility.
        """
        profile = UserProfile.query.filter_by(user_id=user_id).first()
        
        if not profile:
            profile = UserProfile(user_id=user_id)
            db.session.add(profile)

        # Map dynamic attributes
        for key, value in kwargs.items():
            if hasattr(profile, key) and value is not None:
                setattr(profile, key, value)
        
        ProfileService.calculate_completeness(profile)
        
        try:
            db.session.commit()
            return profile, None
        except Exception as e:
            db.session.rollback()
            return None, str(e)

    @staticmethod
    def sync_skills(user_id, skill_list):
        """
        Synchronizes a list of skills (usually from the SkillExtractor).
        Replaces or updates skills in a single transaction.
        """
        try:
            # For simplicity, we'll update or add. 
            # In a full sync, you might want to remove skills not in the list.
            for skill_data in skill_list:
                name = skill_data.get('name', '').strip().lower()
                if not name: continue

                skill = UserSkill.query.filter_by(user_id=user_id, skill_name=name).first()
                if skill:
                    skill.skill_level = skill_data.get('level', skill.skill_level)
                else:
                    new_skill = UserSkill(
                        user_id=user_id,
                        skill_name=name,
                        skill_level=skill_data.get('level', 'intermediate')
                    )
                    db.session.add(new_skill)
            
            db.session.commit()
            return True, None
        except Exception as e:
            db.session.rollback()
            return False, str(e)

    @staticmethod
    def calculate_completeness(profile):
        """
        More granular completeness score including skill count.
        """
        score = 0
        fields = ['education_level', 'branch', 'experience_years', 'preferred_domains']
        
        # Check basic fields (15% each = 60%)
        for field in fields:
            if getattr(profile, field):
                score += 15
        
        # Check skills (40% if user has at least 5 skills)
        skill_count = UserSkill.query.filter_by(user_id=profile.user_id).count()
        score += min(40, skill_count * 8) 
        
        profile.profile_completeness = min(100, score)
        return profile.profile_completeness