from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .user import User
from .profile import UserProfile, UserSkill
from .job import Job, JobSkill
from .recommendation import Recommendation
from .resume import Resume

__all__ = ['db', 'User', 'UserProfile', 'UserSkill', 'Job', 'JobSkill', 'Recommendation', 'Resume']
