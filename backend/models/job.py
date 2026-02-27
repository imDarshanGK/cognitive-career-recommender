from . import db
from datetime import datetime, timezone

class Job(db.Model):
    __tablename__ = 'jobs'
    
    id = db.Column(db.Integer, primary_key=True)
    job_title = db.Column(db.String(255), nullable=False, index=True)
    description = db.Column(db.Text)
    domain = db.Column(db.String(100), nullable=False, index=True)  # AI, Web, Data Science, etc.
    experience_level = db.Column(db.String(50), default='intermediate')
    average_salary = db.Column(db.String(100))
    job_market_demand = db.Column(db.Float, default=1.0)
    
    # Relationships
    # backref='job' is good, but back_populates is more explicit for modern SQLAlchemy
    skills = db.relationship('JobSkill', backref='job', cascade='all, delete-orphan', lazy='joined')
    recommendations = db.relationship('Recommendation', backref='job', cascade='all, delete-orphan')
    
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    
    def to_dict(self):
        return {
            'id': self.id,
            'job_title': self.job_title,
            'description': self.description,
            'domain': self.domain,
            'experience_level': self.experience_level,
            'average_salary': self.average_salary,
            'job_market_demand': self.job_market_demand,
            'required_skills': [s.to_dict() for s in self.skills],
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class JobSkill(db.Model):
    __tablename__ = 'job_skills'
    
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey('jobs.id'), nullable=False, index=True)
    skill_name = db.Column(db.String(255), nullable=False, index=True)
    required_level = db.Column(db.String(50), default='intermediate')
    is_mandatory = db.Column(db.Boolean, default=True)
    
    __table_args__ = (db.UniqueConstraint('job_id', 'skill_name', name='uq_job_skill'),)
    
    def to_dict(self):
        return {
            'skill_name': self.skill_name,
            'required_level': self.required_level,
            'is_mandatory': self.is_mandatory
        }