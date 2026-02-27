from . import db
from datetime import datetime, timezone
import bcrypt

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(500), nullable=False)
    role = db.Column(db.String(50), default='user')  # user or admin
    
    # Email Verification
    email_verified = db.Column(db.Boolean, default=False)
    email_verification_token = db.Column(db.String(128), nullable=True)
    
    # Account Security
    failed_login_attempts = db.Column(db.Integer, default=0)
    lockout_until = db.Column(db.DateTime, nullable=True)

    # Timestamps
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    
    # Relationships
    # uselist=False creates a 1-to-1 relationship
    profile = db.relationship('UserProfile', backref='user', uselist=False, cascade='all, delete-orphan')
    resume = db.relationship('Resume', backref='user', uselist=False, cascade='all, delete-orphan')
    # 1-to-many relationships
    skills = db.relationship('UserSkill', backref='user', cascade='all, delete-orphan')
    recommendations = db.relationship('Recommendation', backref='user', cascade='all, delete-orphan')

    def set_password(self, password):
        """Hash and set password using bcrypt with automatic salting"""
        salt = bcrypt.gensalt()
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

    def verify_password(self, password):
        """Verify password and check lockout status"""
        if self.lockout_until and datetime.now(timezone.utc) < self.lockout_until.replace(tzinfo=timezone.utc):
            return False
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))
    
    def to_dict(self):
        """Convert user instance to dictionary for API responses"""
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'role': self.role,
            'email_verified': self.email_verified,
            'is_locked': self.lockout_until is not None and datetime.now(timezone.utc) < self.lockout_until.replace(tzinfo=timezone.utc),
            'created_at': self.created_at.isoformat() if self.created_at else None
        }