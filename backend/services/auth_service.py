"""
Authentication Service
Handles user registration, login, and JWT token generation
"""

from models import db, User
from datetime import datetime, timedelta, timezone
import jwt
import os
import secrets

class AuthService:
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-change-in-production')
    
    @staticmethod
    def register(name, email, password):
        """
        Register a new user with email verification
        Returns: (user, error, verification_token)
        """
        # Normalizing email
        email = email.lower().strip()
        
        # Check if user exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return None, "Email already registered", None

        # Generate verification token
        verification_token = secrets.token_urlsafe(32)

        # Create new user
        user = User(
            name=name,
            email=email,
            email_verified=False,
            email_verification_token=verification_token
        )
        user.set_password(password)

        try:
            db.session.add(user)
            db.session.commit()
            return user, None, verification_token
        except Exception as e:
            db.session.rollback()
            return None, f"Database error: {str(e)}", None
    
    @staticmethod
    def login(email, password):
        """
        Login user and generate JWT token
        Returns: (token, error)
        """
        user = User.query.filter_by(email=email.lower().strip()).first()
        
        if not user:
            return None, "Invalid email or password"

        # Check for account lockout
        if user.lockout_until and datetime.now(timezone.utc) < user.lockout_until.replace(tzinfo=timezone.utc):
            return None, "Account temporarily locked. Please try again later."
        
        if not user.verify_password(password):
            # Logic for incrementing failed_login_attempts would go here
            return None, "Invalid email or password"
        
        # Reset failed attempts on successful login
        user.failed_login_attempts = 0
        db.session.commit()
        
        # Generate JWT token
        token = AuthService.generate_token(user.id)
        return token, None
    
    @staticmethod
    def generate_token(user_id, expires_in_days=30):
        """Generate JWT token for user"""
        payload = {
            'user_id': user_id,
            'exp': datetime.now(timezone.utc) + timedelta(days=expires_in_days),
            'iat': datetime.now(timezone.utc)
        }
        token = jwt.encode(payload, AuthService.SECRET_KEY, algorithm='HS256')
        
        # Handle cases where jwt.encode might return bytes (older PyJWT versions)
        if isinstance(token, bytes):
            return token.decode('utf-8')
        return token
    
    @staticmethod
    def verify_token(token):
        """
        Verify JWT token
        Returns: (user_id, error)
        """
        try:
            payload = jwt.decode(token, AuthService.SECRET_KEY, algorithms=['HS256'])
            return payload['user_id'], None
        except jwt.ExpiredSignatureError:
            return None, "Token expired"
        except jwt.InvalidTokenError:
            return None, "Invalid token"
    
    @staticmethod
    def get_user_from_token(token):
        """Get user object from token"""
        user_id, error = AuthService.verify_token(token)
        if error:
            return None, error
        
        user = db.session.get(User, user_id) # Modern SQLAlchemy 2.0 style
        if not user:
            return None, "User not found"
        
        return user, None