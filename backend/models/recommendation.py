from . import db
from datetime import datetime

class Recommendation(db.Model):
    __tablename__ = 'recommendations'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    job_id = db.Column(db.Integer, db.ForeignKey('jobs.id'), nullable=False, index=True)
    
    # Matching score (0-100)
    match_score = db.Column(db.Float, nullable=False)
    
    # XAI Data (JSON)
    matched_skills = db.Column(db.Text)  # JSON array
    missing_skills = db.Column(db.Text)  # JSON array
    reasoning = db.Column(db.Text)  # Explanation text
    
    # Roadmap (JSON)
    learning_path = db.Column(db.Text)  # JSON array of steps
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        import json
        return {
            'id': self.id,
            'user_id': self.user_id,
            'job_id': self.job_id,
            'job_title': self.job.job_title if self.job else None,
            'match_score': self.match_score,
            'matched_skills': json.loads(self.matched_skills) if self.matched_skills else [],
            'missing_skills': json.loads(self.missing_skills) if self.missing_skills else [],
            'reasoning': self.reasoning,
            'learning_path': json.loads(self.learning_path) if self.learning_path else [],
            'created_at': self.created_at.isoformat()
        }
