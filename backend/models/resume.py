from . import db
from datetime import datetime

class Resume(db.Model):
    __tablename__ = 'resumes'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True, unique=True)
    
    # File info
    filename = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(500), nullable=False)
    file_type = db.Column(db.String(50))  # pdf, docx
    
    # Extracted data (JSON)
    raw_text = db.Column(db.Text)  # Raw extracted text
    parsed_data = db.Column(db.Text)  # JSON: {skills, experience, education, etc.}
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        import json
        return {
            'id': self.id,
            'filename': self.filename,
            'file_type': self.file_type,
            'parsed_data': json.loads(self.parsed_data) if self.parsed_data else {},
            'created_at': self.created_at.isoformat()
        }
