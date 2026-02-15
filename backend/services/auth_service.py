"""
Authentication Service
Handles user registration, login, and JWT token generation
"""

from models import db, User
from datetime import datetime, timedelta
import jwt
import os

class AuthService:
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-change-in-production')
    
    @staticmethod
    def register(name, email, password):
        """
        Register a new user
        Returns: (user, error)
        """
        # Check if user exists
        existing_user = User.query.filter_by(email=email.lower()).first()
        if existing_user:
            return None, "Email already registered"
        
        # Create new user
        user = User(
            name=name,
            email=email.lower()
        )
        user.set_password(password)
        
        try:
            db.session.add(user)
            db.session.commit()
            return user, None
        except Exception as e:
            db.session.rollback()
            return None, str(e)
    
    @staticmethod
    def login(email, password):
        """
        Login user and generate JWT token
        Returns: (token, error)
        """
        user = User.query.filter_by(email=email.lower()).first()
        
        if not user or not user.verify_password(password):
            return None, "Invalid email or password"
        
        # Generate JWT token
        token = AuthService.generate_token(user.id)
        return token, None
    
    @staticmethod
    def generate_token(user_id, expires_in_days=30):
        """Generate JWT token for user"""
        payload = {
            'user_id': user_id,
            'exp': datetime.utcnow() + timedelta(days=expires_in_days),
            'iat': datetime.utcnow()
        }
        token = jwt.encode(payload, AuthService.SECRET_KEY, algorithm='HS256')
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
        
        user = User.query.get(user_id)
        if not user:
            return None, "User not found"
        
        return user, None
