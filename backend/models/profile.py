from . import db
from datetime import datetime

class UserProfile(db.Model):
    __tablename__ = 'user_profiles'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    
    # Basic Info
    education_level = db.Column(db.String(100))  # High School, Bachelor's, Master's, PhD
    branch = db.Column(db.String(255))  # CSE, Mechanical, etc.
    experience_years = db.Column(db.Float, default=0)
    
    # Interests (comma-separated or JSON array)
    preferred_domains = db.Column(db.Text)  # AI, Web, Data Science, Cloud, etc.
    
    # Profile completeness
    profile_completeness = db.Column(db.Float, default=0)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'education_level': self.education_level,
            'branch': self.branch,
            'experience_years': self.experience_years,
            'preferred_domains': self.preferred_domains,
            'profile_completeness': self.profile_completeness
        }


class UserSkill(db.Model):
    __tablename__ = 'user_skills'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    skill_name = db.Column(db.String(255), nullable=False, index=True)
    skill_level = db.Column(db.String(50), default='intermediate')  # beginner, intermediate, expert
    years_experience = db.Column(db.Float, default=0)
    
    __table_args__ = (db.UniqueConstraint('user_id', 'skill_name', name='uq_user_skill'),)
    
    def to_dict(self):
        return {
            'id': self.id,
            'skill_name': self.skill_name,
            'skill_level': self.skill_level,
            'years_experience': self.years_experience
        }
