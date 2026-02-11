"""
Cognitive Career & Job Recommendation System with Explainable and Adaptive AI
Main Flask Application Entry Point
"""

from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
import os
import hashlib
import secrets
from datetime import datetime
from ai_engine.cognitive_engine import CognitiveRecommendationEngine
from nlp_processor.resume_analyzer import ResumeAnalyzer
from utils.data_processor import DataProcessor
from config import Config

app = Flask(__name__,
            template_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'frontend', 'templates'),
            static_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'frontend', 'static'))
app.config.from_object(Config)

# Set proper secret key for sessions
app.secret_key = secrets.token_hex(32)

# Initialize AI components with error handling
try:
    cognitive_engine = CognitiveRecommendationEngine()
except Exception as e:
    print(f"Warning: Could not initialize CognitiveRecommendationEngine: {e}")
    cognitive_engine = None

try:
    resume_analyzer = ResumeAnalyzer()
except Exception as e:
    print(f"Warning: Could not initialize ResumeAnalyzer: {e}")
    resume_analyzer = None

try:
    data_processor = DataProcessor()
except Exception as e:
    print(f"Warning: Could not initialize DataProcessor: {e}")
    data_processor = None

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
        
        # Process resume using NLP
        resume_data = resume_analyzer.extract_information(file)
        return jsonify(resume_data)
    
    return render_template('upload_resume.html')

@app.route('/analyze_profile', methods=['POST'])
@login_required
def analyze_profile():
    """Analyze user profile and generate recommendations"""
    user_data = request.get_json()
    
    # Add user context from session
    user_data['user_id'] = session.get('user_id')
    user_data['user_info'] = users_db.get(session['user_id'], {})
    
    # Cognitive AI processing flow
    # 1. Observe - Collect user input
    observed_data = cognitive_engine.observe(user_data)
    
    # 2. Understand - Process and contextualize
    understood_context = cognitive_engine.understand(observed_data)
    
    # 3. Analyze - Feature extraction and pattern recognition
    analyzed_features = cognitive_engine.analyze(understood_context)
    
    # 4. Reason - Apply cognitive reasoning
    reasoning_results = cognitive_engine.reason(analyzed_features)
    
    # 5. Decide - Generate recommendations
    recommendations = cognitive_engine.decide(reasoning_results)
    
    # 6. Explain - Provide explainable AI output
    explanations = cognitive_engine.explain(recommendations)
    
    return jsonify({
        'recommendations': recommendations,
        'explanations': explanations,
        'reasoning_flow': reasoning_results
    })

@app.route('/feedback', methods=['POST'])
@login_required
def collect_feedback():
    """Collect user feedback for adaptive learning"""
    feedback_data = request.get_json()
    
    # Add user context
    feedback_data['user_id'] = session.get('user_id')
    feedback_data['timestamp'] = datetime.utcnow().isoformat()
    
    # Learn from feedback
    cognitive_engine.learn(feedback_data)
    
    return jsonify({'status': 'Feedback received and processed'})

@app.route('/api/skills', methods=['GET'])
def get_skills_data():
    """API endpoint for skills analysis"""
    skills_data = data_processor.get_skills_taxonomy()
    return jsonify(skills_data)

@app.route('/api/jobs', methods=['GET'])
def get_jobs_data():
    """API endpoint for job market data"""
    jobs_data = data_processor.get_job_market_data()
    return jsonify(jobs_data)

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
