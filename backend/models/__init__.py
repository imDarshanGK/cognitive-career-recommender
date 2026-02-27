"""
Models Module Initialization
Centralizes database models for the Career Recommendation System
"""

from flask_sqlalchemy import SQLAlchemy

# Initialize the database object
db = SQLAlchemy()

# Import models to register them with SQLAlchemy
from .user import User
from .profile import UserProfile, UserSkill
from .job import Job, JobSkill
from .recommendation import Recommendation
from .resume import Resume

# Define the public API for this package
__all__ = [
    'db', 
    'User', 
    'UserProfile', 
    'UserSkill', 
    'Job', 
    'JobSkill', 
    'Recommendation', 
    'Resume'
]