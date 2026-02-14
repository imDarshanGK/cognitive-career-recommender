"""
Cognitive Career & Job Recommendation System with Explainable and Adaptive AI
Main Flask Application Entry Point
"""

from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
import os
import sys
import hashlib
import secrets
import sqlite3
from datetime import datetime

# Add backend directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ai_engine.cognitive_engine import CognitiveRecommendationEngine
from services.career_matcher import match_roles
from nlp_processor.resume_analyzer import ResumeAnalyzer
from nlp_processor.resume_analyzer_simple import ResumeAnalyzer as SimpleResumeAnalyzer
from utils.data_processor import DataProcessor
from config import Config

app = Flask(__name__,
            template_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'frontend', 'templates'),
            static_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'frontend', 'static'))
app.config.from_object(Config)

# Set proper secret key for sessions
app.secret_key = secrets.token_hex(32)

FEEDBACK_DB = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'instance', 'feedback.db')


def _init_feedback_db():
    os.makedirs(os.path.dirname(FEEDBACK_DB), exist_ok=True)
    with sqlite3.connect(FEEDBACK_DB) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS feedback (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                role TEXT NOT NULL,
                feedback TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )


def _save_feedback(user_id, role, feedback):
    with sqlite3.connect(FEEDBACK_DB) as conn:
        conn.execute(
            "INSERT INTO feedback (user_id, role, feedback, created_at) VALUES (?, ?, ?, ?)",
            (user_id, role, feedback, datetime.utcnow().isoformat())
        )


def _get_feedback_history(user_id, limit=20):
    with sqlite3.connect(FEEDBACK_DB) as conn:
        cursor = conn.execute(
            "SELECT role, feedback, created_at FROM feedback WHERE user_id = ? ORDER BY id DESC LIMIT ?",
            (user_id, limit)
        )
        rows = cursor.fetchall()

    return [
        {
            'role': row[0],
            'feedback': row[1],
            'created_at': row[2]
        }
        for row in rows
    ]

# Initialize AI components with error handling
try:
    cognitive_engine = CognitiveRecommendationEngine()
except Exception as e:
    print(f"Warning: Could not initialize CognitiveRecommendationEngine: {e}")
    cognitive_engine = None

# Initialize resume analyzer with fallback to simple version
try:
    resume_analyzer = ResumeAnalyzer()
    print("✓ ResumeAnalyzer initialized successfully")
except Exception as e:
    print(f"Warning: Could not initialize ResumeAnalyzer ({e}), using SimpleResumeAnalyzer instead")
    try:
        resume_analyzer = SimpleResumeAnalyzer()
        print("✓ SimpleResumeAnalyzer initialized successfully")
    except Exception as e2:
        print(f"Warning: Could not initialize SimpleResumeAnalyzer: {e2}")
        resume_analyzer = None

try:
    data_processor = DataProcessor()
except Exception as e:
    print(f"Warning: Could not initialize DataProcessor: {e}")
    data_processor = None

_init_feedback_db()

# In-memory user storage (replace with database in production)
users_db = {
    'admin@example.com': {
        'password_hash': hashlib.sha256('admin123'.encode()).hexdigest(),
        'first_name': 'Admin',
        'last_name': 'User',
        'email': 'admin@example.com'
    }
}

def hash_password(password):
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password, password_hash):
    """Verify password against hash"""
    return hash_password(password) == password_hash


def _build_structured_profile(resume_data):
    """Normalize resume analyzer output into a simple structured profile"""
    if not resume_data or isinstance(resume_data, dict) is False:
        return {}

    raw = resume_data
    if 'data' in resume_data:
        raw = resume_data.get('data', {})

    skills = []
    if 'skills' in resume_data:
        if isinstance(resume_data['skills'], dict):
            skills.extend(resume_data['skills'].get('technical_skills', []))
            skills.extend(resume_data['skills'].get('soft_skills', []))
        elif isinstance(resume_data['skills'], list):
            skills.extend(resume_data['skills'])

    if raw.get('skills'):
        skills.extend(raw.get('skills'))

    skills = [str(skill).strip() for skill in skills if str(skill).strip()]

    education = {}
    if resume_data.get('education'):
        education = resume_data.get('education')
    elif raw.get('education'):
        education = raw.get('education')

    experience = []
    if resume_data.get('experience'):
        experience = resume_data.get('experience')
    elif raw.get('experience'):
        experience = raw.get('experience')

    interests = resume_data.get('interests') or raw.get('interests') or []

    return {
        'skills': skills,
        'education': education,
        'experience': experience,
        'interests': interests
    }

def login_required(f):
    """Decorator to require login for protected routes"""
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

@app.route('/')
def index():
    """Home page with system overview"""
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user login"""
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        
        if not email or not password:
            flash('Email and password are required', 'error')
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({
                    'success': False,
                    'message': 'Email and password are required'
                }), 400
            return render_template('auth/login.html'), 400
        
        user = users_db.get(email)
        if user and verify_password(password, user['password_hash']):
            session['user_id'] = email
            session['user_name'] = f"{user['first_name']} {user['last_name']}"
            flash('Login successful!', 'success')
            return jsonify({
                'success': True, 
                'redirect_url': '/dashboard',
                'message': 'Login successful!'
            })
        else:
            flash('Invalid email or password', 'error')
            return jsonify({
                'success': False,
                'message': 'Invalid email or password'
            }), 401
    
    return render_template('auth/login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Handle user registration"""
    if request.method == 'POST':
        first_name = request.form.get('first_name', '').strip()
        last_name = request.form.get('last_name', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        
        # Validation
        errors = []
        if not first_name:
            errors.append('First name is required')
        if not last_name:
            errors.append('Last name is required')
        if not email or '@' not in email:
            errors.append('Valid email is required')
        if not password or len(password) < 8:
            errors.append('Password must be at least 8 characters long')
        if password != confirm_password:
            errors.append('Passwords do not match')
        if email in users_db:
            errors.append('Email is already registered')
        
        if errors:
            return jsonify({
                'success': False,
                'errors': errors
            }), 400
        
        # Create new user
        users_db[email] = {
            'password_hash': hash_password(password),
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'created_at': datetime.utcnow().isoformat()
        }
        
        # Auto-login after registration
        session['user_id'] = email
        session['user_name'] = f"{first_name} {last_name}"
        
        return jsonify({
            'success': True,
            'redirect_url': '/dashboard',
            'message': 'Account created successfully!'
        })
    
    return render_template('auth/register.html')

@app.route('/logout')
def logout():
    """Handle user logout"""
    session.clear()
    flash('You have been logged out successfully', 'info')
    return redirect(url_for('index'))

@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    """Handle forgot password requests"""
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        
        if email in users_db:
            # In a real app, you'd send an email with reset link
            flash('Password reset instructions have been sent to your email.', 'info')
            return jsonify({
                'success': True,
                'message': 'Password reset instructions sent to your email.'
            })
        else:
            flash('Email address not found.', 'error')
            return jsonify({
                'success': False,
                'message': 'Email address not found.'
            }), 404
    
    return render_template('auth/forgot_password.html')

@app.route('/dashboard')
@login_required
def dashboard():
    """User dashboard (protected route)"""
    user = users_db.get(session['user_id'], {})
    return render_template('dashboard/index.html', user=user)

@app.route('/upload_resume', methods=['GET', 'POST'])
@login_required
def upload_resume():
    """Handle resume upload and analysis"""
    if request.method == 'POST':
        if 'resume' not in request.files:
            return jsonify({'error': 'No resume file uploaded'})
        
        file = request.files['resume']
        if file.filename == '':
            return jsonify({'error': 'No file selected'})
        
        # Process resume using NLP if available
        if not resume_analyzer:
            return jsonify({'error': 'Resume analyzer is not available. Please use manual input.'}), 503
        
        try:
            resume_data = resume_analyzer.extract_information(file)
            structured_profile = _build_structured_profile(resume_data)
            return jsonify({
                'resume_data': resume_data,
                'structured_profile': structured_profile
            })
        except Exception as e:
            return jsonify({'error': f'Failed to parse resume: {str(e)}'}), 400
    
    return render_template('upload_resume.html')

@app.route('/analyze_profile', methods=['POST'])
@login_required
def analyze_profile():
    """Analyze user profile and generate recommendations"""
    user_data = request.get_json()

    if not user_data:
        return jsonify({'error': 'Missing profile data'}), 400

    match_results = match_roles(user_data)

    return jsonify({
        'recommendations': match_results['recommendations'],
        'normalized_profile': match_results['normalized_profile']
    })

@app.route('/feedback', methods=['POST'])
@login_required
def collect_feedback():
    """Collect user feedback for adaptive learning"""
    feedback_data = request.get_json()
    
    if not feedback_data:
        return jsonify({'error': 'Missing feedback data'}), 400

    user_id = session.get('user_id')
    role = feedback_data.get('role', '').strip()
    feedback = feedback_data.get('feedback', '').strip()

    if not role or not feedback:
        return jsonify({'error': 'Role and feedback are required'}), 400

    _save_feedback(user_id, role, feedback)

    feedback_data['user_id'] = user_id
    feedback_data['timestamp'] = datetime.utcnow().isoformat()

    if cognitive_engine:
        cognitive_engine.learn(feedback_data)

    return jsonify({'status': 'Feedback received and processed'})


@app.route('/api/feedback', methods=['GET'])
@login_required
def get_feedback_history():
    """Return feedback history for the current user"""
    user_id = session.get('user_id')
    history = _get_feedback_history(user_id)
    return jsonify({'history': history})

@app.route('/api/skills', methods=['GET'])
def get_skills_data():
    """API endpoint for skills analysis"""
    if not data_processor:
        return jsonify({'error': 'Skills service temporarily unavailable'}), 503
    skills_data = data_processor.get_skills_taxonomy()
    return jsonify(skills_data if skills_data else {})

@app.route('/api/jobs', methods=['GET'])
def get_jobs_data():
    """API endpoint for job market data"""
    if not data_processor:
        return jsonify({'error': 'Jobs service temporarily unavailable'}), 503
    jobs_data = data_processor.get_job_market_data()
    return jsonify(jobs_data if jobs_data else {})

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('errors/500.html'), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
