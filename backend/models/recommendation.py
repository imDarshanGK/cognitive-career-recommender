from . import db
from datetime import datetime, timezone
import json

class Recommendation(db.Model):
    __tablename__ = 'recommendations'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    job_id = db.Column(db.Integer, db.ForeignKey('jobs.id'), nullable=False, index=True)
    
    # Matching score (0-100 or 0.0-1.0)
    match_score = db.Column(db.Float, nullable=False)
    
    # XAI Data (Stored as JSON strings)
    matched_skills = db.Column(db.Text)  # JSON array
    missing_skills = db.Column(db.Text)  # JSON array
    reasoning = db.Column(db.Text)       # Explanation text
    
    # Roadmap (Stored as JSON string)
    learning_path = db.Column(db.Text)   # JSON array of steps
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    
    def to_dict(self):
        """
        Converts the model instance to a dictionary, 
        parsing JSON strings back into Python lists/objects.
        """
        def safe_json_load(data):
            if not data:
                return []
            try:
                return json.loads(data)
            except (json.JSONDecodeError, TypeError):
                return []

        return {
            'id': self.id,
            'user_id': self.user_id,
            'job_id': self.job_id,
            'job_title': self.job.job_title if hasattr(self, 'job') and self.job else "Unknown Job",
            'match_score': self.match_score,
            'matched_skills': safe_json_load(self.matched_skills),
            'missing_skills': safe_json_load(self.missing_skills),
            'reasoning': self.reasoning,
            'learning_path': safe_json_load(self.learning_path),
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }