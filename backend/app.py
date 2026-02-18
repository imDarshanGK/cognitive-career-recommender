"""
Cognitive Career & Job Recommendation System with Explainable and Adaptive AI
Main Flask Application Entry Point
"""

from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
from flask_wtf.csrf import CSRFProtect, generate_csrf, CSRFError
from werkzeug.utils import secure_filename
import os
import sys
import bcrypt
import secrets
import sqlite3
import logging
import tempfile
import shutil
from functools import wraps
from datetime import datetime

# Add backend directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ai_engine.cognitive_engine import CognitiveRecommendationEngine
from services.career_matcher import match_roles
from nlp_processor.resume_analyzer import ResumeAnalyzer
from nlp_processor.resume_analyzer_simple import SimpleResumeAnalyzer
from utils.data_processor import DataProcessor
from config import Config

app = Flask(__name__,
            template_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'frontend', 'templates'),
            static_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'frontend', 'static'))
app.config.from_object(Config)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler('app.log'), logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

# CSRF protection for forms and JSON requests
csrf = CSRFProtect(app)

# Ensure secret key is consistent with configuration
app.secret_key = app.config.get('SECRET_KEY') or secrets.token_hex(32)

@app.context_processor
def inject_csrf_token():
    return {'csrf_token': generate_csrf}

# Security headers middleware
@app.after_request
def add_security_headers(response):
    """Add security headers to all responses"""
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    # CORS headers - allow frontend requests
    origin = request.origin or request.host or 'http://localhost'
    response.headers['Access-Control-Allow-Origin'] = origin
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, X-Requested-With, X-CSRFToken'
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    # Content Security Policy
    response.headers['Content-Security-Policy'] = (
        "default-src 'self'; "
        "script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
        "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://fonts.googleapis.com; "
        "font-src 'self' https://cdn.jsdelivr.net https://fonts.gstatic.com; "
        "img-src 'self' data: https:; "
        "connect-src 'self' https:; "
        "frame-ancestors 'none'"
    )
    return response

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
            "SELECT id, role, feedback, created_at FROM feedback WHERE user_id = ? ORDER BY id DESC LIMIT ?",
            (user_id, limit)
        )
        rows = cursor.fetchall()

    return [
        {
            'id': row[0],
            'role': row[1],
            'feedback': row[2],
            'created_at': row[3]
        }
        for row in rows
    ]

def _delete_feedback(user_id, feedback_id):
    """Delete a specific feedback entry"""
    try:
        with sqlite3.connect(FEEDBACK_DB) as conn:
            # First check if feedback belongs to this user
            cursor = conn.execute(
                "SELECT id FROM feedback WHERE id = ? AND user_id = ?",
                (feedback_id, user_id)
            )
            if not cursor.fetchone():
                return False
            
            # Delete the feedback
            conn.execute(
                "DELETE FROM feedback WHERE id = ? AND user_id = ?",
                (feedback_id, user_id)
            )
            conn.commit()
            return True
    except Exception as e:
        logger.error(f"Error deleting feedback: {e}")
        return False

# Initialize AI components with error handling
try:
    cognitive_engine = CognitiveRecommendationEngine()
    logger.info("CognitiveRecommendationEngine initialized successfully")
except Exception as e:
    logger.warning(f"Could not initialize CognitiveRecommendationEngine: {e}")
    cognitive_engine = None

# Initialize resume analyzers with fallback
resume_analyzer = None
simple_analyzer = None

try:
    resume_analyzer = ResumeAnalyzer()
    logger.info("ResumeAnalyzer initialized successfully")
except Exception as e:
    logger.warning(f"Could not initialize ResumeAnalyzer: {e}")

# Always initialize simple analyzer as fallback
try:
    simple_analyzer = SimpleResumeAnalyzer()
    logger.info("SimpleResumeAnalyzer initialized successfully")
    if not resume_analyzer:
        resume_analyzer = simple_analyzer  # Use simple as primary if main failed
        logger.info("Using SimpleResumeAnalyzer as primary analyzer")
except Exception as e:
    logger.warning(f"Could not initialize SimpleResumeAnalyzer: {e}")

try:
    data_processor = DataProcessor()
    logger.info("DataProcessor initialized successfully")
except Exception as e:
    logger.warning(f"Could not initialize DataProcessor: {e}")
    data_processor = None

_init_feedback_db()

# In-memory user storage (replace with database in production)
users_db = {
    'admin@example.com': {
        'password_hash': bcrypt.hashpw('admin123'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
        'first_name': 'Admin',
        'last_name': 'User',
        'email': 'admin@example.com'
    }
}

def hash_password(password):
    """Hash password using bcrypt with automatic salting"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(password, password_hash):
    """Verify password against hash - FIXED: bcrypt.checkpw expects bytes"""
    try:
        # Convert password to bytes
        password_bytes = password.encode('utf-8')
        # password_hash might be str or bytes - convert to bytes if needed
        if isinstance(password_hash, str):
            password_hash_bytes = password_hash.encode('utf-8')
        else:
            password_hash_bytes = password_hash
        return bcrypt.checkpw(password_bytes, password_hash_bytes)
    except (ValueError, TypeError) as e:
        logger.error(f"Password verification error: {e}")
        return False


def _build_structured_profile(resume_data):
    """Normalize resume analyzer output into a simple structured profile"""
    if not resume_data or isinstance(resume_data, dict) is False:
        return {}

    # Handle nested data structure from resume analyzers
    raw = resume_data
    if 'data' in resume_data:
        raw = resume_data.get('data', {})

    skills = []
    
    # Extract skills from various possible locations
    if 'skills' in resume_data:
        if isinstance(resume_data['skills'], dict):
            skills.extend(resume_data['skills'].get('technical_skills', []))
            skills.extend(resume_data['skills'].get('soft_skills', []))
        elif isinstance(resume_data['skills'], list):
            skills.extend(resume_data['skills'])
    
    # Check data.skills
    if raw.get('skills'):
        raw_skills = raw.get('skills')
        if isinstance(raw_skills, dict):
            skills.extend(raw_skills.get('technical_skills', []))
            skills.extend(raw_skills.get('soft_skills', []))
        elif isinstance(raw_skills, list):
            skills.extend(raw_skills)

    # Filter out noise - keep only technical skills
    VALID_TECH_SKILLS = {
        'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'ruby', 'php', 'go', 'rust', 'kotlin', 'swift',
        'html', 'css', 'react', 'angular', 'vue', 'node', 'express', 'django', 'flask', 'spring', 'laravel',
        'sql', 'mysql', 'postgresql', 'mongodb', 'redis', 'oracle', 'sqlite',
        'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'jenkins', 'git', 'gitlab', 'github',
        'linux', 'unix', 'bash', 'shell', 'powershell',
        'rest', 'api', 'graphql', 'soap', 'microservices',
        'machine learning', 'ml', 'ai', 'deep learning', 'tensorflow', 'pytorch', 'keras', 'scikit-learn', 'sklearn',
        'pandas', 'numpy', 'matplotlib', 'seaborn',
        'data analysis', 'data science', 'statistics', 'excel', 'tableau', 'powerbi',
        'testing', 'junit', 'pytest', 'selenium', 'cypress', 'jest',
        'agile', 'scrum', 'jira', 'ci/cd', 'devops'
    }
    
    filtered_skills = []
    for skill in skills:
        skill_clean = str(skill).strip().lower()
        # Remove parentheticals and punctuation
        skill_clean = skill_clean.replace('(', '').replace(')', '').replace('-', ' ')
        # Check if it's a known technical skill or contains one
        if skill_clean in VALID_TECH_SKILLS or any(tech in skill_clean for tech in VALID_TECH_SKILLS):
            filtered_skills.append(skill_clean)
    
    # Clean and deduplicate skills
    skills = list(set(filtered_skills))
    
    logger.debug(f"Extracted {len(skills)} skills after filtering: {skills[:15]}")

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

    result = {
        'skills': skills,
        'education': education,
        'experience': experience,
        'interests': interests
    }
    
    logger.debug(f"Final profile - skills count: {len(result['skills'])}")
    return result

def login_required(f):
    """Decorator to require login for protected routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
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
    user_email = session.get('user_id')
    user = users_db.get(user_email, {})
    
    # Log user access
    logger.info(f"Dashboard accessed by user: {user_email}")
    
    # Ensure user has all required fields
    if not user:
        user = {'email': user_email, 'first_name': '', 'last_name': ''}
    
    # Get or construct first name
    first_name = user.get('first_name', '').strip()
    last_name = user.get('last_name', '').strip()
    email = user.get('email', user_email)
    
    # If first_name is empty, try to extract from email
    if not first_name and email:
        # Extract part before @ sign, capitalize it
        email_part = email.split('@')[0]
        first_name = email_part.replace('.', ' ').replace('_', ' ').title()
    
    # Ensure we have values
    user['first_name'] = first_name or 'User'
    user['last_name'] = last_name
    user['email'] = email or user_email
    
    logger.debug(f"User profile loaded: {user['first_name']} {user.get('last_name')}")
    
    return render_template('dashboard/index.html', user=user)

@app.route('/upload_resume', methods=['GET', 'POST'])
@login_required
def upload_resume():
    """Handle resume upload and analysis"""
    if request.method == 'POST':
        max_size = app.config.get('MAX_CONTENT_LENGTH')
        if max_size and request.content_length and request.content_length > max_size:
            return jsonify({'error': 'File size exceeds the allowed limit.'}), 413

        if 'resume' not in request.files:
            return jsonify({'error': 'No resume file uploaded'}), 400
        
        file = request.files['resume']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Validate file extension and MIME type - FIXED: now requires both checks
        allowed_extensions = app.config.get('ALLOWED_EXTENSIONS', {'pdf', 'doc', 'docx', 'txt'})
        
        # Check if filename has extension
        if '.' not in file.filename:
            return jsonify({'error': 'File must have an extension (.pdf, .doc, .docx, or .txt)'}), 400
        
        file_ext = file.filename.rsplit('.', 1)[1].lower()
        
        # Prevent double extensions like .pdf.exe
        if len(file_ext) > 4 or file_ext not in allowed_extensions:
            return jsonify({'error': f'Invalid file type. Allowed types: {', '.join(sorted(allowed_extensions))}'}), 400

        allowed_mime_types = {
            'application/pdf',
            'application/msword',
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            'text/plain'
        }
        if file.mimetype and file.mimetype not in allowed_mime_types:
            logger.warning(f"File {file.filename} has suspicious MIME type: {file.mimetype}")
            return jsonify({'error': 'Invalid file content type.'}), 400

        file.filename = secure_filename(file.filename)
        
        # Save to temporary file for processing
        temp_dir = tempfile.mkdtemp(prefix='resume_', dir=app.config.get('UPLOAD_FOLDER'))
        temp_file_path = os.path.join(temp_dir, file.filename)
        
        try:
            file.save(temp_file_path)
        except Exception as e:
            logger.error(f"Failed to save uploaded file: {e}")
            shutil.rmtree(temp_dir, ignore_errors=True)
            return jsonify({'error': 'Failed to save file'}), 500
        
        # Try primary analyzer first
        resume_data = None
        try:
            if resume_analyzer:
                try:
                    with open(temp_file_path, 'rb') as f:
                        # Attach filename attribute so analyzer can determine file type
                        f.filename = file.filename
                        resume_data = resume_analyzer.extract_information(f)
                    if resume_data and not resume_data.get('error'):
                        structured_profile = _build_structured_profile(resume_data)
                        logger.info(f"Resume parsed successfully using primary analyzer")
                        return jsonify({
                            'resume_data': resume_data,
                            'structured_profile': structured_profile
                        })
                except Exception as e:
                    logger.warning(f"Primary analyzer failed: {e}, trying fallback...")
            
            # Fallback to simple analyzer if available
            if simple_analyzer:
                try:
                    with open(temp_file_path, 'rb') as f:
                        # Attach filename attribute so analyzer can determine file type
                        f.filename = file.filename
                        resume_data = simple_analyzer.extract_information(f)
                    structured_profile = _build_structured_profile(resume_data)
                    logger.info(f"Resume parsed successfully using fallback analyzer")
                    return jsonify({
                        'resume_data': resume_data,
                        'structured_profile': structured_profile
                    })
                except Exception as e:
                    logger.error(f"Fallback analyzer also failed: {e}")
            
            logger.error(f"Both analyzers failed for file: {file.filename}")
            return jsonify({'error': 'Failed to parse resume. Please try manual profile entry.'}), 400
        finally:
            # Clean up temporary files
            try:
                shutil.rmtree(temp_dir, ignore_errors=True)
                logger.debug(f"Cleaned up temporary directory: {temp_dir}")
            except Exception as e:
                logger.warning(f"Failed to clean up temp directory: {e}")
    
    return render_template('upload_resume.html')

@app.route('/analyze_profile', methods=['POST'])
@login_required
def analyze_profile():
    """Analyze user profile and generate recommendations"""
    try:
        user_data = request.get_json()
    except Exception as e:
        return jsonify({'error': 'Invalid JSON data'}), 400

    if not user_data:
        return jsonify({'error': 'Missing profile data'}), 400

    try:
        match_results = match_roles(user_data)
    except Exception as e:
        return jsonify({'error': f'Error analyzing profile: {str(e)}'}), 500

    return jsonify({
        'recommendations': match_results['recommendations'],
        'normalized_profile': match_results['normalized_profile'],
        'market_skills': match_results.get('market_skills', {})
    })

@app.route('/feedback', methods=['POST'])
@login_required
def collect_feedback():
    """Collect user feedback for adaptive learning"""
    try:
        feedback_data = request.get_json()
    except Exception as e:
        return jsonify({'error': 'Invalid JSON data'}), 400
    
    if not feedback_data:
        return jsonify({'error': 'Missing feedback data'}), 400

    user_id = session.get('user_id')
    role = feedback_data.get('role', '').strip()
    feedback = feedback_data.get('feedback', '').strip()

    if not role or not feedback:
        return jsonify({'error': 'Role and feedback are required'}), 400

    try:
        _save_feedback(user_id, role, feedback)
    except Exception as e:
        return jsonify({'error': f'Error saving feedback: {str(e)}'}), 500

    feedback_data['user_id'] = user_id
    feedback_data['timestamp'] = datetime.utcnow().isoformat()

    if cognitive_engine:
        try:
            cognitive_engine.learn(feedback_data)
        except Exception as e:
            # Log error but don't fail the request
            logger.warning(f"Could not process feedback with cognitive engine: {e}")

    return jsonify({'status': 'Feedback received and processed'})


@app.route('/api/feedback', methods=['GET'])
@login_required
def get_feedback_history():
    """Return feedback history for the current user"""
    user_id = session.get('user_id')
    history = _get_feedback_history(user_id)
    logger.debug(f"Loaded {len(history)} feedback entries for user {user_id}")
    return jsonify({'history': history})

@app.route('/api/feedback/<int:feedback_id>', methods=['DELETE'])
@login_required
def delete_feedback_entry(feedback_id):
    """Delete a specific feedback entry"""
    user_id = session.get('user_id')
    
    if _delete_feedback(user_id, feedback_id):
        logger.info(f"Deleted feedback {feedback_id} for user {user_id}")
        return jsonify({'status': 'Feedback deleted successfully'})
    else:
        logger.warning(f"Failed to delete feedback {feedback_id} for user {user_id}")
        return jsonify({'error': 'Feedback not found or unauthorized'}), 404

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
    filters = {
        'query': request.args.get('query', '').strip(),
        'location': request.args.get('location', '').strip(),
        'results': request.args.get('results', type=int)
    }
    jobs_data = data_processor.get_job_market_data(filters)
    return jsonify(jobs_data if jobs_data else {})

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('errors/500.html'), 500

@app.errorhandler(CSRFError)
def handle_csrf_error(error):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({'error': 'Invalid or missing CSRF token.'}), 400
    return render_template('errors/500.html', error_message='Invalid or missing CSRF token.'), 400

if __name__ == '__main__':
    debug_mode = os.environ.get('DEBUG', 'False').lower() in ('true', '1', 't')
    app.run(debug=debug_mode, host='0.0.0.0', port=5000)
