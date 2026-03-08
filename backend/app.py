
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
import smtplib
import re
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from functools import wraps
from datetime import datetime, timezone, timedelta

# Add backend directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ai_engine.cognitive_engine import CognitiveRecommendationEngine
from services.career_matcher import match_roles
from nlp_processor.resume_analyzer import ResumeAnalyzer
from nlp_processor.resume_analyzer_simple import SimpleResumeAnalyzer
from utils.data_processor import DataProcessor
from config import Config
from models import db, User, UserProfile, UserSkill
from services.auth_service import AuthService

app = Flask(__name__,
            template_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'frontend', 'templates'),
            static_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'frontend', 'static'))
app.config.from_object(Config)
Config.init_app(app)
db.init_app(app)

with app.app_context():
    db.create_all()

# Resend verification email route (moved here so 'app' is defined)
@app.route('/resend-verification', methods=['POST'])
def resend_verification():
    email = request.form.get('email', '').strip().lower()
    user = User.query.filter_by(email=email).first()
    if not user:
        flash('User not found.', 'error')
        return redirect(url_for('verify_email_notice', email=email))
    if user.email_verified:
        flash('Email already verified. Please log in.', 'info')
        return redirect(url_for('login'))
    # Generate new token
    verification_token = secrets.token_urlsafe(32)
    user.email_verification_token = verification_token
    db.session.commit()
    mail_username = (app.config.get('MAIL_USERNAME') or '').strip()
    mail_password = (app.config.get('MAIL_PASSWORD') or '').strip()
    mail_configured = bool(mail_username and mail_password and mail_username != 'your-email@gmail.com')
    first_name = (user.name or '').split(' ')[0] if user.name else ''
    verification_url = url_for('verify_email', token=verification_token, _external=True)
    mail_sent = False

    otp_code = _generate_email_otp()
    _save_email_otp(email, otp_code)

    mail_status = 'not_configured'
    if mail_configured:
        mail_sent = send_verification_email(email, verification_token, first_name, otp_code)
        if mail_sent:
            mail_status = 'sent'
            flash('Verification email resent. Please check your inbox.', 'success')
        else:
            mail_status = 'delivery_failed'
            flash('Could not send verification email. Please check email settings.', 'warning')
    else:
        logger.warning(f"EMAIL NOT CONFIGURED - Verification URL: {verification_url}")
        flash('Email service is not configured in this environment.', 'info')

    notice_args = {
        'email': email,
        'success': 1,
        'mail_sent': 1 if mail_sent else 0,
        'mail_status': mail_status,
    }
    if not mail_sent and app.config.get('DEBUG'):
        notice_args['verification_url'] = verification_url
        notice_args['otp_hint'] = otp_code

    return redirect(url_for('verify_email_notice', **notice_args))

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
OTP_EXPIRY_MINUTES = 10


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
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS email_otp (
                email TEXT PRIMARY KEY,
                otp_code TEXT NOT NULL,
                expires_at TEXT NOT NULL
            )
            """
        )


def _save_feedback(user_id, role, feedback):
    with sqlite3.connect(FEEDBACK_DB) as conn:
        conn.execute(
            "INSERT INTO feedback (user_id, role, feedback, created_at) VALUES (?, ?, ?, ?)",
            (user_id, role, feedback, datetime.now(timezone.utc).isoformat())
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


def _generate_email_otp():
    return ''.join(str(secrets.randbelow(10)) for _ in range(6))


def _save_email_otp(email, otp_code):
    expires_at = (datetime.now(timezone.utc) + timedelta(minutes=OTP_EXPIRY_MINUTES)).isoformat()
    with sqlite3.connect(FEEDBACK_DB) as conn:
        conn.execute(
            """
            INSERT INTO email_otp (email, otp_code, expires_at)
            VALUES (?, ?, ?)
            ON CONFLICT(email) DO UPDATE SET
                otp_code = excluded.otp_code,
                expires_at = excluded.expires_at
            """,
            (email, otp_code, expires_at)
        )


def _delete_email_otp(email):
    with sqlite3.connect(FEEDBACK_DB) as conn:
        conn.execute("DELETE FROM email_otp WHERE email = ?", (email,))


def _verify_email_otp(email, otp_code):
    with sqlite3.connect(FEEDBACK_DB) as conn:
        cursor = conn.execute(
            "SELECT otp_code, expires_at FROM email_otp WHERE email = ?",
            (email,)
        )
        row = cursor.fetchone()

    if not row:
        return False, 'No OTP found for this email. Please request a new OTP.'

    saved_code, expires_at_raw = row
    if str(saved_code).strip() != str(otp_code).strip():
        return False, 'Invalid OTP code. Please try again.'

    try:
        expires_at = datetime.fromisoformat(expires_at_raw)
    except ValueError:
        _delete_email_otp(email)
        return False, 'OTP is invalid. Please request a new one.'

    if expires_at.tzinfo is None:
        expires_at = expires_at.replace(tzinfo=timezone.utc)

    if datetime.now(timezone.utc) > expires_at:
        _delete_email_otp(email)
        return False, 'OTP expired. Please request a new OTP.'

    _delete_email_otp(email)
    return True, None

def send_verification_email(email, verification_token, first_name, otp_code=None):
    """Send email verification link to user"""
    try:
        # Check if email configuration is available
        mail_username = app.config.get('MAIL_USERNAME')
        mail_password = app.config.get('MAIL_PASSWORD')
        
        if not mail_username or not mail_password or mail_username == 'your-email@gmail.com':
            logger.warning(f"Email not configured. Skipping email send for {email}. Token: {verification_token}")
            return False
        
        # Create verification link
        verification_link = f"http://localhost:5000/verify-email/{verification_token}"
        
        # Create email message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = 'Verify Your Email - CareerAI'
        msg['From'] = app.config.get('MAIL_DEFAULT_SENDER')
        msg['To'] = email
        
        # HTML version of email
        html_content = f"""
        <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <div style="max-width: 600px; margin: 0 auto;">
                    <div style="background: linear-gradient(135deg, #1b3a6b, #275395); color: white; padding: 30px; border-radius: 8px 8px 0 0; text-align: center;">
                        <h1 style="margin: 0; font-size: 28px;">CareerAI</h1>
                        <p style="margin: 5px 0 0 0; font-size: 14px;">Verify Your Email</p>
                    </div>
                    
                    <div style="padding: 30px; background: #f5f7fa; border-radius: 0 0 8px 8px;">
                        <h2 style="color: #1b3a6b; margin-top: 0;">Hello {first_name},</h2>
                        
                        <p>Thank you for creating an account with CareerAI! To get started with your personalized career recommendations, please verify your email address by clicking the link below or using the OTP code.</p>

                        <div style="margin: 14px 0 24px 0; padding: 14px; background: #ffffff; border: 1px dashed #275395; border-radius: 8px; text-align: center;">
                            <div style="font-size: 13px; color: #555; margin-bottom: 6px;">Your verification OTP</div>
                            <div style="font-size: 28px; letter-spacing: 4px; font-weight: 700; color: #1b3a6b;">{otp_code or ''}</div>
                            <div style="font-size: 12px; color: #666; margin-top: 6px;">Valid for {OTP_EXPIRY_MINUTES} minutes</div>
                        </div>
                        
                        <div style="text-align: center; margin: 30px 0;">
                            <a href="{verification_link}" style="display: inline-block; background: linear-gradient(135deg, #1b3a6b, #275395); color: white; padding: 12px 30px; text-decoration: none; border-radius: 6px; font-weight: bold; font-size: 16px;">
                                Verify Email Address
                            </a>
                        </div>
                        
                        <hr style="border: none; border-top: 1px solid #ddd; margin: 20px 0;">
                        
                        <p style="color: #666; font-size: 13px;">
                            This verification link will expire in 1 hour. If you didn't create this account, you can safely ignore this email.
                        </p>
                        
                        <p style="color: #999; font-size: 12px; margin-top: 20px;">
                            Best regards,<br>
                            <strong>CareerAI Team</strong>
                        </p>
                    </div>
                </div>
            </body>
        </html>
        """
        
        # Plain text version
        text_content = f"""
        Hello {first_name},
        
        Thank you for creating an account with CareerAI! To get started with your personalized career recommendations, please verify your email address using the button in this email or the OTP code:

        OTP: {otp_code or ''}
        
        This verification link will expire in 1 hour. If you didn't create this account, you can safely ignore this email.
        
        Best regards,
        CareerAI Team
        """
        
        # Attach both versions
        msg.attach(MIMEText(text_content, 'plain'))
        msg.attach(MIMEText(html_content, 'html'))
        
        # Send email via SMTP
        try:
            server = smtplib.SMTP(app.config.get('MAIL_SERVER'), app.config.get('MAIL_PORT'))
            server.starttls()
            server.login(mail_username, mail_password)
            server.send_message(msg)
            server.quit()
            logger.info(f"Verification email sent successfully to {email}")
            return True
        except smtplib.SMTPAuthenticationError:
            logger.error(f"SMTP authentication failed. Check MAIL_USERNAME and MAIL_PASSWORD in .env")
            return False
        except smtplib.SMTPException as e:
            logger.error(f"SMTP error sending email to {email}: {e}")
            return False
            
    except Exception as e:
        logger.error(f"Error sending verification email to {email}: {e}")
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

    # Filter out obvious noise while preserving real resume terms.
    blocked_tokens = {
        'skills',
        'technical skills',
        'soft skills',
        'summary',
        'profile',
        'experience',
        'education',
        'certifications',
        'projects',
        'responsibilities',
        'curriculum vitae',
        'resume',
    }

    cleaned_skills = []
    for skill in skills:
        skill_clean = str(skill).strip().lower()
        if not skill_clean:
            continue

        skill_clean = skill_clean.replace('(', '').replace(')', '').replace('-', ' ')
        skill_clean = ' '.join(skill_clean.split())

        # Reject noise-like entries and keep realistic short skill phrases.
        if skill_clean in blocked_tokens:
            continue
        if len(skill_clean) < 2 or len(skill_clean) > 50:
            continue
        if any(ch in skill_clean for ch in ['\n', '\r', '\t', ':', ';']):
            continue

        cleaned_skills.append(skill_clean)

    # Deduplicate while preserving order.
    skills = list(dict.fromkeys(cleaned_skills))

    # Fallback: extract known skills from raw resume text when parser skill arrays are sparse.
    if len(skills) < 2:
        known_skills = {
            'python', 'sql', 'data analysis', 'machine learning', 'tensorflow', 'pytorch',
            'pandas', 'numpy', 'statistics', 'excel', 'tableau', 'powerbi', 'aws', 'azure',
            'gcp', 'docker', 'kubernetes', 'linux', 'django', 'flask', 'fastapi', 'javascript',
            'typescript', 'react', 'node', 'html', 'css', 'api', 'microservices', 'ci/cd',
            'git', 'java', 'c++', 'c#', 'go', 'rust', 'angular', 'vue'
        }

        text_candidates = []
        for key in ['resume_text', 'text', 'summary', 'objective']:
            if resume_data.get(key):
                text_candidates.append(str(resume_data.get(key)))
            if isinstance(raw, dict) and raw.get(key):
                text_candidates.append(str(raw.get(key)))

        # Include serialized payload as last resort for simple keyword scan.
        text_blob = ' '.join(text_candidates) + ' ' + json.dumps(resume_data)
        text_blob = text_blob.lower()

        extracted_from_text = []
        for skill in sorted(known_skills, key=len, reverse=True):
            pattern = r'\b' + re.escape(skill) + r'\b'
            if re.search(pattern, text_blob):
                extracted_from_text.append(skill)

        if extracted_from_text:
            skills = list(dict.fromkeys(skills + extracted_from_text))
    
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


def _normalize_skill_tokens(raw_skills):
    if not raw_skills:
        return []
    if isinstance(raw_skills, str):
        tokens = raw_skills.split(',')
    elif isinstance(raw_skills, list):
        tokens = raw_skills
    else:
        return []

    cleaned = []
    for token in tokens:
        text = str(token).strip()
        if text:
            cleaned.append(text)
    # Deduplicate while preserving order.
    return list(dict.fromkeys(cleaned))


def _extract_years(profile_payload):
    experience = profile_payload.get('experience', []) if isinstance(profile_payload, dict) else []
    total = 0.0
    if isinstance(experience, list):
        for entry in experience:
            try:
                total += float(entry.get('years', 0))
            except (TypeError, ValueError, AttributeError):
                continue
    return total


def _save_user_profile_snapshot(user, profile_payload):
    """Persist a normalized profile snapshot for dashboard auto-restore."""
    if not user or not isinstance(profile_payload, dict):
        return

    skills = _normalize_skill_tokens(profile_payload.get('skills', []))
    interests = _normalize_skill_tokens(profile_payload.get('interests', []))
    years = _extract_years(profile_payload)

    education_level = None
    education = profile_payload.get('education', {})
    if isinstance(education, dict):
        degrees = education.get('degrees', [])
        if isinstance(degrees, list) and degrees:
            education_level = str(degrees[0]).strip() or None

    profile = UserProfile.query.filter_by(user_id=user.id).first()
    if not profile:
        profile = UserProfile(user_id=user.id)
        db.session.add(profile)

    profile.education_level = education_level
    profile.experience_years = years
    profile.preferred_domains = ', '.join(interests)

    completeness = 0
    if education_level:
        completeness += 25
    if years > 0:
        completeness += 25
    if skills:
        completeness += 35
    if interests:
        completeness += 15
    profile.profile_completeness = float(min(100, completeness))

    # Replace skill rows with latest snapshot.
    UserSkill.query.filter_by(user_id=user.id).delete(synchronize_session=False)
    for skill in skills:
        db.session.add(UserSkill(user_id=user.id, skill_name=skill, years_experience=years))

    db.session.commit()


def _load_user_profile_snapshot(user):
    """Build dashboard-friendly payload from persisted DB profile tables."""
    if not user:
        return None

    profile = UserProfile.query.filter_by(user_id=user.id).first()
    skills = UserSkill.query.filter_by(user_id=user.id).all()

    skill_names = [s.skill_name for s in skills if s.skill_name]
    interests = []
    years = 0.0
    education_level = ''

    if profile:
        interests = [x.strip() for x in (profile.preferred_domains or '').split(',') if x.strip()]
        years = float(profile.experience_years or 0)
        education_level = (profile.education_level or '').strip()

    if not skill_names and not interests and years <= 0 and not education_level:
        return None

    return {
        'skills': skill_names,
        'interests': interests,
        'education': {'degrees': [education_level] if education_level else []},
        'experience': [{'years': years}] if years > 0 else []
    }

def login_required(f):
    """Decorator to require login AND email verification for protected routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        
        # Verify user still exists and email is verified
        user_id = session.get('user_id')
        user = users_db.get(user_id)
        if not user or not user.get('email_verified', False):
            session.clear()
            flash('Session expired or email not verified. Please log in again.', 'error')
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
        session.clear()  # Always clear session on login attempt
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

        user = User.query.filter_by(email=email).first()
        now = datetime.now(timezone.utc)

        # Account lockout logic
        if user:
            # Check if account is locked
            if user.lockout_until and user.lockout_until > now:
                session.clear()
                remaining = int((user.lockout_until - now).total_seconds() // 60) + 1
                return jsonify({
                    'success': False,
                    'message': f'Account locked due to too many failed attempts. Try again in {remaining} minutes.'
                }), 403
            if user.verify_password(password):
                if not user.email_verified:
                    session.clear()
                    return jsonify({
                        'success': False,
                        'message': 'Please verify your email before logging in. Check your email for verification link.'
                    }), 403
                # Reset failed attempts on successful login
                user.failed_login_attempts = 0
                user.lockout_until = None
                from models import db
                db.session.commit()
                session['user_id'] = user.email
                session['user_name'] = user.name
                session.permanent = True
                flash('Login successful!', 'success')
                return jsonify({
                    'success': True,
                    'redirect_url': '/dashboard',
                    'message': 'Login successful!'
                })
            else:
                # Increment failed attempts
                user.failed_login_attempts = (user.failed_login_attempts or 0) + 1
                if user.failed_login_attempts >= 5:
                    user.lockout_until = now + timedelta(minutes=15)
                from models import db
                db.session.commit()
        session.clear()  # Always clear session on failed login
        flash('Invalid email or password', 'error')
        return jsonify({
            'success': False,
            'message': 'Invalid email or password'
        }), 401

    return render_template('auth/login.html')

def validate_password_strength(password):
    """
    Validate password strength requirements:
    - 8+ characters
    - At least 1 uppercase letter
    - At least 1 number
    - At least 1 special character
    """
    import re
    
    errors = []
    if len(password) < 8:
        errors.append('Password must be at least 8 characters long')
    if not re.search(r'[A-Z]', password):
        errors.append('Password must contain at least one uppercase letter')
    if not re.search(r'[0-9]', password):
        errors.append('Password must contain at least one number')
    if not re.search(r'[!@#$%^&*()_+\-=\[\]{};:\'",.<>?/\\|`~]', password):
        errors.append('Password must contain at least one special character (!@#$%^&* etc.)')
    
    return errors

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Handle user registration (DB-backed, with email verification)"""
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.accept_mimetypes['application/json'] > request.accept_mimetypes['text/html']
    if request.method == 'POST':
        first_name = request.form.get('first_name', '').strip()
        last_name = request.form.get('last_name', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        errors = []
        if not first_name:
            errors.append('First name is required')
        if not last_name:
            errors.append('Last name is required')
        if not email or '@' not in email:
            errors.append('Valid email is required')
        if not password:
            errors.append('Password is required')
        else:
            password_errors = validate_password_strength(password)
            errors.extend(password_errors)
        if password != confirm_password:
            errors.append('Passwords do not match')
        if User.query.filter_by(email=email).first():
            errors.append('Email is already registered')
        if errors:
            if is_ajax:
                return jsonify({'success': False, 'errors': errors}), 400
            else:
                return render_template('auth/register.html', errors=errors)

        # Register user (email_verified=False, token generated)
        user, err, verification_token = AuthService.register(f"{first_name} {last_name}", email, password)
        if err:
            if is_ajax:
                return jsonify({'success': False, 'errors': [err]}), 400
            else:
                return render_template('auth/register.html', errors=[err])

        mail_username = (app.config.get('MAIL_USERNAME') or '').strip()
        mail_password = (app.config.get('MAIL_PASSWORD') or '').strip()
        mail_configured = bool(mail_username and mail_password and mail_username != 'your-email@gmail.com')
        verification_url = url_for('verify_email', token=verification_token, _external=True)
        otp_code = _generate_email_otp()
        _save_email_otp(email, otp_code)
        mail_sent = False
        mail_status = 'not_configured'
        if mail_configured:
            mail_sent = send_verification_email(email, verification_token, first_name, otp_code)
            mail_status = 'sent' if mail_sent else 'delivery_failed'
            if not mail_sent:
                logger.warning(f"EMAIL DELIVERY FAILED - Verification URL: {verification_url}")
        else:
            logger.warning(f"EMAIL NOT CONFIGURED - Verification URL: {verification_url}")

        notice_args = {
            'success': 1,
            'email': email,
            'mail_sent': 1 if mail_sent else 0,
            'mail_status': mail_status,
        }
        if not mail_sent and app.config.get('DEBUG'):
            notice_args['verification_url'] = verification_url
            notice_args['otp_hint'] = otp_code

        notice_url = url_for('verify_email_notice', **notice_args)
        if is_ajax:
            message = (
                'Account created! Verification email sent. Please check your inbox.'
                if mail_sent
                else 'Account created, but verification email could not be delivered right now. Use OTP or resend email from the next page.'
            )
            return jsonify({
                'success': True,
                'redirect_url': notice_url,
                'message': message
            })
        return redirect(notice_url)
    # Always return JSON for AJAX GET requests
    if is_ajax:
        return jsonify({'success': False, 'message': 'GET not supported for registration'}), 405
    return render_template('auth/register.html')

@app.route('/logout')
def logout():
    """Handle user logout - clear all session and authentication data"""
    session.clear()
    response = jsonify({
        'success': True,
        'message': 'You have been logged out successfully'
    })
    response.set_cookie('session', '', expires=0)
    flash('You have been logged out successfully', 'info')
    return redirect(url_for('index'))

@app.route('/verify-email-notice')
def verify_email_notice():
    """Show email verification notice"""
    return render_template('auth/verify_email_notice.html')

@app.route('/verify-email/<token>')
def verify_email(token):
    """Verify user email with token (DB-backed)"""
    user = User.query.filter_by(email_verification_token=token, email_verified=False).first()
    if user:
        user.email_verified = True
        user.email_verification_token = None
        db.session.commit()
        _delete_email_otp(user.email)
        flash('Email verified successfully! Please complete your profile.', 'success')
        session['user_id'] = user.email
        # Redirect to profile setup page after verification
        return redirect(url_for('profile'))
    flash('Invalid or expired verification link.', 'error')
    return redirect(url_for('index'))


@app.route('/verify-email-code', methods=['POST'])
def verify_email_code():
    """Verify user email with a 6-digit OTP code."""
    email = request.form.get('email', '').strip().lower()
    otp_code = request.form.get('otp_code', '').strip()

    if not email or not otp_code:
        flash('Email and OTP code are required.', 'error')
        return redirect(url_for('verify_email_notice', email=email, mail_sent=request.args.get('mail_sent', 0)))

    user = User.query.filter_by(email=email, email_verified=False).first()
    if not user:
        flash('User not found or already verified.', 'error')
        return redirect(url_for('login'))

    valid, reason = _verify_email_otp(email, otp_code)
    if not valid:
        flash(reason or 'Invalid OTP code.', 'error')
        return redirect(url_for('verify_email_notice', email=email, success=1, mail_sent=1))

    user.email_verified = True
    user.email_verification_token = None
    db.session.commit()

    flash('Email verified successfully using OTP! Please complete your profile.', 'success')
    session['user_id'] = user.email
    return redirect(url_for('profile'))
# Profile setup route
def db_login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        user = User.query.filter_by(email=session['user_id']).first()
        if not user or not user.email_verified:
            session.clear()
            flash('Session expired or email not verified. Please log in again.', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/profile', methods=['GET', 'POST'])
@db_login_required
def profile():
    user_email = session.get('user_id')
    user = User.query.filter_by(email=user_email).first()
    if request.method == 'POST':
        profession = request.form.get('profession', '').strip()
        if profession:
            # Save profession or other profile fields
            # (Assuming a profession field exists in User or UserProfile)
            flash('Profile updated successfully!', 'success')
    return render_template('auth/profile.html', user=user)

@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    """Handle forgot password requests"""
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()

        user_exists = User.query.filter_by(email=email).first() is not None
        if user_exists:
            # In a real app, you would send a reset email here.
            logger.info(f"Password reset requested for {email}")

        flash('If this email is registered, password reset instructions have been sent.', 'info')
        return jsonify({
            'success': True,
            'message': 'If this email is registered, password reset instructions have been sent.'
        })
    
    return render_template('auth/forgot_password.html')

@app.route('/dashboard')
@db_login_required
def dashboard():
    """User dashboard (protected route, DB-backed)"""
    user_email = session.get('user_id')
    user = User.query.filter_by(email=user_email).first()
    logger.info(f"Dashboard accessed by user: {user_email}")
    return render_template('dashboard/index.html', user=user)


@app.route('/api/profile/current', methods=['GET'])
@db_login_required
def get_current_profile():
    """Return persisted profile snapshot for dashboard auto-load."""
    user_email = session.get('user_id')
    user = User.query.filter_by(email=user_email).first()
    profile_payload = _load_user_profile_snapshot(user)
    return jsonify({'has_profile': bool(profile_payload), 'profile': profile_payload or {}})


@app.route('/api/profile/current', methods=['DELETE'])
@db_login_required
def clear_current_profile():
    """Delete persisted profile snapshot for the current user."""
    user_email = session.get('user_id')
    user = User.query.filter_by(email=user_email).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404

    UserSkill.query.filter_by(user_id=user.id).delete(synchronize_session=False)
    UserProfile.query.filter_by(user_id=user.id).delete(synchronize_session=False)
    db.session.commit()

    return jsonify({'status': 'Profile cleared'})

@app.route('/upload_resume', methods=['GET', 'POST'])
@db_login_required
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
                        user_email = session.get('user_id')
                        user = User.query.filter_by(email=user_email).first() if user_email else None
                        if user:
                            _save_user_profile_snapshot(user, structured_profile)
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
                    user_email = session.get('user_id')
                    user = User.query.filter_by(email=user_email).first() if user_email else None
                    if user:
                        _save_user_profile_snapshot(user, structured_profile)
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
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({'error': 'Use POST to upload a resume.'}), 405
    return redirect(url_for('dashboard'))

@app.route('/analyze_profile', methods=['POST'])
@db_login_required
def analyze_profile():
    """Analyze user profile and generate recommendations"""
    try:
        user_data = request.get_json()
    except Exception as e:
        return jsonify({'error': 'Invalid JSON data'}), 400

    if not user_data:
        return jsonify({'error': 'Missing profile data'}), 400

    user_email = session.get('user_id')
    user = User.query.filter_by(email=user_email).first()
    if user:
        try:
            _save_user_profile_snapshot(user, user_data)
        except Exception as e:
            logger.warning(f"Could not persist user profile snapshot: {e}")

    try:
        match_results = match_roles(user_data)
    except Exception as e:
        return jsonify({'error': f'Error analyzing profile: {str(e)}'}), 500

    return jsonify({
        'recommendations': match_results['recommendations'],
        'normalized_profile': match_results['normalized_profile'],
        'skill_gap': match_results.get('skill_gap', []),
        'roadmap': match_results.get('roadmap', []),
        'market_skills': match_results.get('market_skills', {}),
        'live_jobs': match_results.get('live_jobs', []),
        'data_source': match_results.get('data_source', ''),
        'data_message': match_results.get('data_message', '')
    })

@app.route('/feedback', methods=['POST'])
@db_login_required
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
    feedback_data['timestamp'] = datetime.now(timezone.utc).isoformat()

    if cognitive_engine:
        try:
            cognitive_engine.learn(feedback_data)
        except Exception as e:
            # Log error but don't fail the request
            logger.warning(f"Could not process feedback with cognitive engine: {e}")

    return jsonify({'status': 'Feedback received and processed'})


@app.route('/api/feedback', methods=['GET'])
@db_login_required
def get_feedback_history():
    """Return feedback history for the current user"""
    user_id = session.get('user_id')
    history = _get_feedback_history(user_id)
    logger.debug(f"Loaded {len(history)} feedback entries for user {user_id}")
    return jsonify({'history': history})

@app.route('/api/feedback/<int:feedback_id>', methods=['DELETE'])
@db_login_required
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
    # Check email configuration on startup
    mail_username = app.config.get('MAIL_USERNAME')
    mail_configured = mail_username and mail_username != 'your-email@gmail.com'
    
    if not mail_configured:
        logger.warning("=" * 80)
        logger.warning("EMAIL SERVICE NOT CONFIGURED - Development Mode Active")
        logger.warning("Users will be auto-verified on registration (no email sent)")
        logger.warning("To enable emails, update .env with:")
        logger.warning("  MAIL_USERNAME=your-actual-email@gmail.com")
        logger.warning("  MAIL_PASSWORD=your-app-specific-password")
        logger.warning("=" * 80)
    else:
        logger.info("Email service configured and ready")
    
    debug_mode = os.environ.get('DEBUG', 'False').lower() in ('true', '1', 't')
    app.run(debug=debug_mode, host='0.0.0.0', port=5000)
