from . import db
from datetime import datetime, timezone
import json

class Resume(db.Model):
    __tablename__ = 'resumes'
    
    id = db.Column(db.Integer, primary_key=True)
    # unique=True enforces a 1:1 relationship between User and Resume
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True, unique=True)
    
    # File info
    filename = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(500), nullable=False)
    file_type = db.Column(db.String(50))  # pdf, docx
    
    # Extracted data
    raw_text = db.Column(db.Text)  # Full text for re-processing
    parsed_data = db.Column(db.Text)  # JSON: {skills: [], experience: [], education: []}
    
    # Modern UTC timestamps
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    
    def to_dict(self):
        """
        Returns summary data for the UI. 
        Excludes raw_text to minimize payload size.
        """
        parsed = {}
        if self.parsed_data:
            try:
                parsed = json.loads(self.parsed_data)
            except (json.JSONDecodeError, TypeError):
                parsed = {"error": "Data format invalid"}

        return {
            'id': self.id,
            'user_id': self.user_id,
            'filename': self.filename,
            'file_type': self.file_type,
            'parsed_data': parsed,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }