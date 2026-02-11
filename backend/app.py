"""
Cognitive Career & Job Recommendation System with Explainable and Adaptive AI
Main Flask Application Entry Point
"""

from flask import Flask, render_template, request, jsonify
import os
from ai_engine.cognitive_engine import CognitiveRecommendationEngine
from nlp_processor.resume_analyzer import ResumeAnalyzer
from utils.data_processor import DataProcessor
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# Initialize AI components
cognitive_engine = CognitiveRecommendationEngine()
resume_analyzer = ResumeAnalyzer()
data_processor = DataProcessor()

@app.route('/')
def index():
    """Home page with system overview"""
    return render_template('index.html')

@app.route('/upload_resume', methods=['GET', 'POST'])
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
def analyze_profile():
    """Analyze user profile and generate recommendations"""
    user_data = request.get_json()
    
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
def collect_feedback():
    """Collect user feedback for adaptive learning"""
    feedback_data = request.get_json()
    
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
