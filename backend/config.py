import os
import re
import secrets
import logging
from datetime import datetime, timezone
from flask import Flask, request, jsonify, session, flash, redirect, url_for
from flask_wtf.csrf import CSRFProtect
from config import Config

# Configure Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- 1. COGNITIVE ENGINE MODULES ---

class SkillExtractor:
    """Uses optimized regex for single-pass skill identification."""
    SKILLS_DB = {
        'Technical': ['Python', 'Java', 'JavaScript', 'C++', 'Go', 'Rust', 'TypeScript', 'SQL', 'NoSQL'],
        'Web & Cloud': ['React', 'Angular', 'Node.js', 'Django', 'Flask', 'AWS', 'Docker', 'Kubernetes'],
        'AI/ML': ['Machine Learning', 'TensorFlow', 'PyTorch', 'Pandas', 'NLP', 'Computer Vision'],
        'DevOps': ['CI/CD', 'Terraform', 'Jenkins', 'Git', 'Ansible']
    }

    def __init__(self):
        # Create mapping and sort by length to prevent partial matches (e.g., Java vs JavaScript)
        self.skill_map = {s.lower(): s for cat in self.SKILLS_DB.values() for s in cat}
        sorted_keys = sorted(self.skill_map.keys(), key=len, reverse=True)
        self.regex = re.compile(r'\b(' + '|'.join(re.escape(s) for s in sorted_keys) + r')\b', re.IGNORECASE)

    def extract(self, text):
        matches = self.regex.findall(text)
        return list({self.skill_map[m.lower()] for m in matches})



class MatchingEngine:
    """Calculates weighted scores with proficiency scaling and mandatory penalties."""
    LEVEL_VALS = {'beginner': 1, 'intermediate': 2, 'expert': 3}

    @staticmethod
    def calculate_score(user_skills, job_reqs):
        if not job_reqs: return 0
        
        score_sum = 0
        total_weight = 0
        mandatory_penalty = 0

        for req in job_reqs:
            name = req['name'].lower()
            weight = 2.0 if req.get('is_mandatory') else 1.0
            total_weight += weight
            
            if name in user_skills:
                u_lvl = MatchingEngine.LEVEL_VALS.get(user_skills[name].lower(), 1)
                r_lvl = MatchingEngine.LEVEL_VALS.get(req['level'].lower(), 1)
                # Score scaling based on proficiency gap
                skill_score = (u_lvl / r_lvl) if u_lvl < r_lvl else 1.0
                score_sum += (skill_score * weight)
            elif req.get('is_mandatory'):
                mandatory_penalty += 15 # Flat penalty for missing core requirement

        final_score = (score_sum / total_weight) * 100
        return max(0, round(final_score - mandatory_penalty, 2))



class XAIExplainer:
    """Generates transparent reasoning for the AI's decision."""
    @staticmethod
    def explain(score, job_title, matched, missing_mandatory):
        if score >= 80:
            status = "Highly Recommended"
            reason = f"Your profile shows strong mastery in {', '.join(matched[:3])}."
        elif missing_mandatory:
            status = "Gap Identified"
            reason = f"While you have the foundation, this role strictly requires: {', '.join(missing_mandatory)}."
        else:
            status = "Potential Match"
            reason = "You meet the basic requirements but could improve proficiency in key areas."
            
        return {"status": status, "narrative": reason, "score": score}

# --- 2. FLASK APPLICATION FACTORY ---

app = Flask(__name__)
app.config.from_object(Config)
Config.init_app(app)
csrf = CSRFProtect(app)

# Initialize AI Components
extractor = SkillExtractor()
engine = MatchingEngine()
explainer = XAIExplainer()

# Mock Database for testing
MOCK_JOBS = [
    {
        "id": 101, "title": "Senior Python Developer", 
        "reqs": [
            {"name": "Python", "level": "expert", "is_mandatory": True},
            {"name": "AWS", "level": "intermediate", "is_mandatory": True},
            {"name": "Docker", "level": "beginner", "is_mandatory": False}
        ]
    }
]

# --- 3. ROUTES ---

@app.route('/')
def home():
    return jsonify({"system": "Cognitive Career AI", "status": "Ready"})

@app.route('/api/upload', methods=['POST'])
def upload_resume():
    if 'resume' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files['resume']
    # Securely read text (In production, use a PDF parser like PyMuPDF)
    raw_text = file.read().decode('utf-8', errors='ignore')
    
    found_skills = extractor.extract(raw_text)
    
    # Store user skills in session (as expert for this demo)
    session['user_profile'] = {s.lower(): 'expert' for s in found_skills}
    session.permanent = True
    
    return jsonify({
        "message": "Resume analyzed",
        "skills_found": found_skills,
        "count": len(found_skills)
    })

@app.route('/api/recommendations', methods=['GET'])
def get_recommendations():
    user_profile = session.get('user_profile')
    if not user_profile:
        return jsonify({"error": "Please upload a resume first"}), 401

    recommendations = []
    for job in MOCK_JOBS:
        score = engine.calculate_score(user_profile, job['reqs'])
        
        # Calculate XAI Gaps
        matched = [r['name'] for r in job['reqs'] if r['name'].lower() in user_profile]
        missing_mandatory = [r['name'] for r in job['reqs'] if r['name'].lower() not in user_profile and r.get('is_mandatory')]
        
        insight = explainer.explain(score, job['title'], matched, missing_mandatory)
        
        recommendations.append({
            "job_id": job['id'],
            "job_title": job['title'],
            "match_score": score,
            "ai_insight": insight
        })

    return jsonify(sorted(recommendations, key=lambda x: x['match_score'], reverse=True))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)