"""
Configuration settings for Cognitive Career & Job Recommendation System
"""

import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Application configuration"""
    
    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'cognitive-ai-career-system-2024'
    DEBUG = os.environ.get('DEBUG', 'False').lower() in ('true', '1', 't')
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = os.environ.get('SESSION_COOKIE_SAMESITE', 'Lax')
    SESSION_COOKIE_SECURE = os.environ.get('SESSION_COOKIE_SECURE', 'False').lower() in ('true', '1', 't')
    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = 3600
    
    # File upload settings
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'data', 'uploads')
    ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'txt'}
    
    # Database settings (if needed for future expansion)
    DATABASE_URL = os.environ.get('DATABASE_URL') or 'sqlite:///career_system.db'
    
    # AI/ML Model settings
    MODEL_PATH = os.path.join(os.path.dirname(__file__), 'models')
    DATA_PATH = os.path.join(os.path.dirname(__file__), 'data')
    
    # Cognitive AI parameters
    REASONING_THRESHOLD = 0.75
    EXPLANATION_DEPTH = 3
    LEARNING_RATE = 0.01
    
    # NLP settings
    SPACY_MODEL = 'en_core_web_sm'
    MAX_RESUME_LENGTH = 10000  # characters
    
    # Job recommendation settings
    MAX_RECOMMENDATIONS = 10
    SIMILARITY_THRESHOLD = 0.6

    # Adzuna API settings for live jobs data
    ADZUNA_APP_ID = os.environ.get('ADZUNA_APP_ID')
    ADZUNA_APP_KEY = os.environ.get('ADZUNA_APP_KEY')
    ADZUNA_COUNTRY = os.environ.get('ADZUNA_COUNTRY', 'in')
    
    # Database configuration
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 10,
        'pool_recycle': 3600,
        'pool_pre_ping': True
    }
    ADZUNA_RESULTS_PER_PAGE = int(os.environ.get('ADZUNA_RESULTS_PER_PAGE', '10'))
    
    # Explainable AI settings
    SHAP_SAMPLE_SIZE = 1000
    LIME_NUM_FEATURES = 20
    
    @staticmethod
    def init_app(app):
        """Initialize app with configuration"""
        # Create necessary directories
        os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
        os.makedirs(Config.MODEL_PATH, exist_ok=True)
        os.makedirs(Config.DATA_PATH, exist_ok=True)
