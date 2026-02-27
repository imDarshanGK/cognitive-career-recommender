from . import db
from datetime import datetime, timezone

class UserProfile(db.Model):
    __tablename__ = 'user_profiles'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    
    # Basic Info
    education_level = db.Column(db.String(100))  # High School, Bachelor's, Master's, PhD
    branch = db.Column(db.String(255))  # CSE, Mechanical, etc.
    experience_years = db.Column(db.Float, default=0)
    
    # Interests
    preferred_domains = db.Column(db.Text)  # Comma-separated: AI, Web, Cloud
    
    # Profile completeness
    profile_completeness = db.Column(db.Float, default=0)
    
    # Timestamps using timezone-aware UTC
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    
    # Relationship for easy access
    # Assumes User model has a relationship back to this
    
    def to_dict(self):
        # Helper to convert comma-separated string to list
        domains = []
        if self.preferred_domains:
            domains = [d.strip() for d in self.preferred_domains.split(',') if d.strip()]

        return {
            'id': self.id,
            'user_id': self.user_id,
            'education_level': self.education_level,
            'branch': self.branch,
            'experience_years': self.experience_years,
            'preferred_domains': domains,
            'profile_completeness': self.profile_completeness,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class UserSkill(db.Model):
    __tablename__ = 'user_skills'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    skill_name = db.Column(db.String(255), nullable=False, index=True)
    skill_level = db.Column(db.String(50), default='intermediate')  # beginner, intermediate, expert
    years_experience = db.Column(db.Float, default=0)
    
    # Prevent duplicate skills for the same user
    __table_args__ = (db.UniqueConstraint('user_id', 'skill_name', name='uq_user_skill'),)
    
    def to_dict(self):
        return {
            'id': self.id,
            'skill_name': self.skill_name,
            'skill_level': self.skill_level,
            'years_experience': self.years_experience
        }