from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__, 
            template_folder=os.path.join(os.path.dirname(__file__), '..', 'frontend', 'templates'),
            static_folder=os.path.join(os.path.dirname(__file__), '..', 'frontend', 'static'))

@app.route('/')
def home():
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>🧠 CareerAI - Cognitive Career & Job Recommendation System</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                font-family: 'Inter', sans-serif;
                display: flex;
                align-items: center;
                justify-content: center;
            }
            .main-container {
                background: rgba(255, 255, 255, 0.98);
                border-radius: 20px;
                box-shadow: 0 20px 50px rgba(0,0,0,0.15);
                backdrop-filter: blur(20px);
                max-width: 1400px;
                width: 98%;
                overflow: hidden;
                animation: slideInUp 0.8s ease;
            }
            
            /* Top Section */
            .hero-section { 
                padding: 3rem 2rem 2rem 2rem; 
                text-align: center; 
                background: white;
            }
            .brain-icon {
                font-size: 4rem;
                background: linear-gradient(45deg, #667eea, #764ba2);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                margin-bottom: 1rem;
                animation: pulse 2s infinite;
            }
            .title { 
                font-size: 2.8rem;
                font-weight: 700;
                color: #2c3e50;
                margin-bottom: 0.5rem;
            }
            .subtitle {
                font-size: 1.2rem;
                color: #5a6c7d;
                font-weight: 500;
                margin-bottom: 0.8rem;
            }
            .tagline {
                font-size: 1rem;
                color: #7f8c8d;
                margin-bottom: 2rem;
            }
            
            /* Buttons */
            .buttons-section { margin-bottom: 1rem; }
            .btn-main {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                border: none;
                padding: 12px 30px;
                font-weight: 600;
                border-radius: 25px;
                color: white;
                text-decoration: none;
                margin: 0.5rem;
                display: inline-block;
                transition: all 0.3s ease;
            }
            .btn-main:hover {
                transform: translateY(-2px);
                box-shadow: 0 10px 25px rgba(102, 126, 234, 0.3);
                color: white;
                text-decoration: none;
            }
            .btn-secondary {
                background: rgba(102, 126, 234, 0.1);
                border: 2px solid #667eea;
                padding: 10px 25px;
                font-weight: 500;
                border-radius: 25px;
                color: #667eea;
                text-decoration: none;
                margin: 0.5rem;
                display: inline-block;
                transition: all 0.3s ease;
            }
            .btn-secondary:hover {
                background: #667eea;
                color: white;
                text-decoration: none;
            }
            
            /* Features Section */
            .features-section {
                background: #f8f9fa;
                padding: 2rem;
                border-top: 1px solid #e9ecef;
            }
            .section-title {
                font-size: 1.4rem;
                font-weight: 600;
                text-align: center;
                margin-bottom: 1.5rem;
                color: #2c3e50;
            }
            .features-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 1rem;
            }
            .feature-item {
                text-align: center;
                padding: 1rem;
            }
            .feature-icon {
                font-size: 2rem;
                margin-bottom: 0.5rem;
            }
            .feature-item:nth-child(1) .feature-icon { color: #e74c3c; }
            .feature-item:nth-child(2) .feature-icon { color: #f39c12; }
            .feature-item:nth-child(3) .feature-icon { color: #27ae60; }
            .feature-title {
                font-weight: 600;
                margin-bottom: 0.25rem;
                color: #2c3e50;
            }
            .feature-desc {
                font-size: 0.9rem;
                color: #6c757d;
                margin: 0;
            }
            
            /* How It Works */
            .workflow-section {
                background: white;
                padding: 2rem;
                border-top: 1px solid #e9ecef;
                text-align: center;
            }
            .workflow-flow {
                font-size: 1rem;
                color: #495057;
                font-weight: 500;
                margin: 1rem 0;
                padding: 1rem;
                background: #f8f9fa;
                border-radius: 10px;
                border-left: 4px solid #667eea;
            }
            
            /* Cognitive AI Loop */
            .cognitive-section {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 2rem;
                text-align: center;
            }
            .cognitive-loop {
                font-size: 1.1rem;
                font-weight: 500;
                margin: 1rem 0;
                padding: 1rem;
                background: rgba(255,255,255,0.1);
                border-radius: 10px;
                backdrop-filter: blur(10px);
            }
            
            /* Footer */
            .footer-section {
                background: #2c3e50;
                color: white;
                padding: 1.5rem;
                text-align: center;
            }
            .footer-title {
                font-weight: 600;
                margin-bottom: 0.5rem;
            }
            .footer-tech {
                font-size: 0.9rem;
                color: #bdc3c7;
            }
            
            /* Animations */
            @keyframes slideInUp {
                from { opacity: 0; transform: translateY(30px); }
                to { opacity: 1; transform: translateY(0); }
            }
            @keyframes pulse {
                0%, 100% { transform: scale(1); }
                50% { transform: scale(1.05); }
            }
            
            /* Responsive */
            @media (max-width: 768px) {
                .main-container { width: 95%; margin: 1rem auto; }
                .title { font-size: 2.2rem; }
                .subtitle { font-size: 1rem; }
                .hero-section { padding: 2rem 1.5rem 1.5rem; }
                .features-section, .workflow-section, .cognitive-section { padding: 1.5rem; }
            }
        </style>
    </head>
    <body>
        <div class="main-container">
            <!-- Hero Section -->
            <div class="hero-section">
                <div class="brain-icon">
                    <i class="fas fa-brain"></i>
                </div>
                <h1 class="title">🧠 CareerAI</h1>
                <h2 class="subtitle">Cognitive Career & Job Recommendation System</h2>
                <p class="tagline">Intelligent career guidance powered by Cognitive and Explainable AI.</p>
                
                <div class="buttons-section">
                    <a href="/login" class="btn-main">🚀 Start Your Journey</a>
                    <a href="/signup" class="btn-secondary">👤 Sign Up Free</a>
                </div>
            </div>
            
            <!-- Core Features -->
            <div class="features-section">
                <h3 class="section-title">Core Features</h3>
                <div class="features-grid">
                    <div class="feature-item">
                        <div class="feature-icon"><i class="fas fa-brain"></i></div>
                        <div class="feature-title">🧠 Cognitive Reasoning</div>
                        <p class="feature-desc">Human-like career decision logic.</p>
                    </div>
                    <div class="feature-item">
                        <div class="feature-icon"><i class="fas fa-search"></i></div>
                        <div class="feature-title">🔍 Explainable AI</div>
                        <p class="feature-desc">Shows why jobs are recommended.</p>
                    </div>
                    <div class="feature-item">
                        <div class="feature-icon"><i class="fas fa-sync-alt"></i></div>
                        <div class="feature-title">🔁 Adaptive Learning</div>
                        <p class="feature-desc">Improves suggestions with feedback.</p>
                    </div>
                </div>
            </div>
            
            <!-- How It Works -->
            <div class="workflow-section">
                <h3 class="section-title">How It Works</h3>
                <div class="workflow-flow">
                    Profile Input → AI Analysis → Cognitive Reasoning → Job Recommendation → Explanation
                </div>
            </div>
            
            <!-- Cognitive AI Loop -->
            <div class="cognitive-section">
                <h3 class="section-title" style="color: white;">🧩 Cognitive AI Loop</h3>
                <div class="cognitive-loop">
                    Observe → Understand → Analyze → Reason → Decide → Explain → Learn
                </div>
            </div>
            
            <!-- Footer -->
            <div class="footer-section">
                <div class="footer-title">Developed as a Cognitive AI Academic Project</div>
                <div class="footer-tech">Technologies: NLP | Machine Learning | Explainable AI</div>
            </div>
        </div>
        
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    </body>
    </html>
    '''

@app.route('/login')
def login():
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>🔐 Login - CareerAI</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; font-family: 'Inter', sans-serif; display: flex; align-items: center; justify-content: center; }
            .login-container { background: white; border-radius: 20px; padding: 3rem; box-shadow: 0 20px 50px rgba(0,0,0,0.1); max-width: 450px; width: 90%; }
            .logo { text-align: center; margin-bottom: 2rem; }
            .brain-icon { font-size: 3rem; color: #667eea; margin-bottom: 1rem; }
            .title { font-size: 2rem; font-weight: 700; color: #2c3e50; margin-bottom: 0.5rem; }
            .subtitle { color: #6c757d; margin-bottom: 2rem; }
            .form-group { margin-bottom: 1.5rem; }
            .form-label { font-weight: 600; color: #2c3e50; margin-bottom: 0.5rem; }
            .form-control { padding: 12px 15px; border: 2px solid #e9ecef; border-radius: 10px; font-size: 1rem; }
            .form-control:focus { border-color: #667eea; box-shadow: 0 0 0 0.2rem rgba(102, 126, 234, 0.25); }
            .btn-primary { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border: none; padding: 12px; font-weight: 600; border-radius: 10px; width: 100%; margin-bottom: 1rem; }
            .btn-primary:hover { transform: translateY(-2px); box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3); }
            .btn-link { color: #667eea; text-decoration: none; }
            .btn-link:hover { color: #5a67d8; }
            .divider { text-align: center; margin: 1.5rem 0; color: #6c757d; }
        </style>
    </head>
    <body>
        <div class="login-container">
            <div class="logo">
                <div class="brain-icon"><i class="fas fa-brain"></i></div>
                <h1 class="title">🧠 CareerAI</h1>
                <p class="subtitle">Login to access your personalized career insights</p>
            </div>
            
            <form action="/auth" method="POST">
                <div class="form-group">
                    <label class="form-label">Email Address</label>
                    <input type="email" class="form-control" name="email" placeholder="Enter your email" required>
                </div>
                
                <div class="form-group">
                    <label class="form-label">Password</label>
                    <input type="password" class="form-control" name="password" placeholder="Enter your password" required>
                </div>
                
                <button type="submit" class="btn btn-primary">🚀 Login & Start Analysis</button>
            </form>
            
            <div class="divider">Don't have an account?</div>
            <div class="text-center">
                <a href="/signup" class="btn-link">👤 Create Free Account</a>
            </div>
            
            <div class="text-center mt-3">
                <a href="/" class="btn-link">← Back to Home</a>
            </div>
        </div>
    </body>
    </html>
    '''

@app.route('/signup')
def signup():
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>📝 Sign Up - CareerAI</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; font-family: 'Inter', sans-serif; display: flex; align-items: center; justify-content: center; }
            .signup-container { background: white; border-radius: 20px; padding: 3rem; box-shadow: 0 20px 50px rgba(0,0,0,0.1); max-width: 500px; width: 90%; }
            .logo { text-align: center; margin-bottom: 2rem; }
            .brain-icon { font-size: 3rem; color: #667eea; margin-bottom: 1rem; }
            .title { font-size: 2rem; font-weight: 700; color: #2c3e50; margin-bottom: 0.5rem; }
            .subtitle { color: #6c757d; margin-bottom: 2rem; }
            .form-group { margin-bottom: 1.5rem; }
            .form-label { font-weight: 600; color: #2c3e50; margin-bottom: 0.5rem; }
            .form-control { padding: 12px 15px; border: 2px solid #e9ecef; border-radius: 10px; font-size: 1rem; }
            .form-control:focus { border-color: #667eea; box-shadow: 0 0 0 0.2rem rgba(102, 126, 234, 0.25); }
            .btn-primary { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border: none; padding: 12px; font-weight: 600; border-radius: 10px; width: 100%; margin-bottom: 1rem; }
            .btn-primary:hover { transform: translateY(-2px); box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3); }
            .btn-link { color: #667eea; text-decoration: none; }
            .btn-link:hover { color: #5a67d8; }
            .divider { text-align: center; margin: 1.5rem 0; color: #6c757d; }
            .row { margin: 0; }
        </style>
    </head>
    <body>
        <div class="signup-container">
            <div class="logo">
                <div class="brain-icon"><i class="fas fa-brain"></i></div>
                <h1 class="title">📝 Join CareerAI</h1>
                <p class="subtitle">Create your account to get personalized career recommendations</p>
            </div>
            
            <form action="/register" method="POST">
                <div class="row">
                    <div class="col-6">
                        <div class="form-group">
                            <label class="form-label">First Name</label>
                            <input type="text" class="form-control" name="first_name" placeholder="John" required>
                        </div>
                    </div>
                    <div class="col-6">
                        <div class="form-group">
                            <label class="form-label">Last Name</label>
                            <input type="text" class="form-control" name="last_name" placeholder="Doe" required>
                        </div>
                    </div>
                </div>
                
                <div class="form-group">
                    <label class="form-label">Email Address</label>
                    <input type="email" class="form-control" name="email" placeholder="john@example.com" required>
                </div>
                
                <div class="form-group">
                    <label class="form-label">Password</label>
                    <input type="password" class="form-control" name="password" placeholder="At least 8 characters" required>
                </div>
                
                <div class="form-group">
                    <label class="form-label">Confirm Password</label>
                    <input type="password" class="form-control" name="confirm_password" placeholder="Re-enter password" required>
                </div>
                
                <button type="submit" class="btn btn-primary">🎯 Create Account & Setup Profile</button>
            </form>
            
            <div class="divider">Already have an account?</div>
            <div class="text-center">
                <a href="/login" class="btn-link">🔐 Login Here</a>
            </div>
            
            <div class="text-center mt-3">
                <a href="/" class="btn-link">← Back to Home</a>
            </div>
        </div>
    </body>
    </html>
    '''

@app.route('/auth', methods=['POST'])
def authenticate():
    # Simulate authentication - In real app, check database
    return '''
    <script>
        alert("✅ Login Successful! Redirecting to Profile Setup...");
        window.location.href = "/profile";
    </script>
    '''

@app.route('/register', methods=['POST'])
def register():
    # Simulate registration - In real app, save to database
    return '''
    <script>
        alert("🎉 Account Created Successfully! Setting up your profile...");
        window.location.href = "/profile";
    </script>
    '''

@app.route('/analyze', methods=['POST'])
def analyze():
    # Simulate profile analysis - In real app, process with AI
    return '''
    <script>
        alert("🧠 AI Analysis Complete! Generating your personalized career recommendations...");
        window.location.href = "/dashboard";
    </script>
    '''

@app.route('/dashboard')
def dashboard():
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Dashboard - CareerAI</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
        <style>
            body { 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                font-family: 'Segoe UI', sans-serif;
            }
            .navbar {
                background: rgba(0,0,0,0.1);
                backdrop-filter: blur(10px);
            }
            .card {
                border: none;
                border-radius: 15px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.1);
                transition: transform 0.3s ease;
            }
            .card:hover { transform: translateY(-5px); }
            .stat-card {
                background: linear-gradient(45deg, #667eea, #764ba2);
                color: white;
            }
            .welcome-section {
                background: rgba(255,255,255,0.95);
                border-radius: 20px;
                backdrop-filter: blur(10px);
                margin: 2rem 0;
                padding: 2rem;
            }
        </style>
    </head>
    <body>
        <!-- Navigation -->
        <nav class="navbar navbar-expand-lg navbar-dark">
            <div class="container">
                <a class="navbar-brand" href="/">
                    <i class="fas fa-brain me-2"></i>CareerAI
                </a>
                <div class="navbar-nav ms-auto">
                    <a class="nav-link" href="/">🏠 Home</a>
                    <a class="nav-link" href="/profile">👤 Profile</a>
                    <a class="nav-link active" href="/dashboard">📊 Dashboard</a>
                    <a class="nav-link" href="/demo">🔍 Demo</a>
                    <a class="nav-link" href="/login">🚪 Logout</a>
                </div>
            </div>
        </nav>
        
        <!-- Main Content -->
        <div class="container mt-4">
            <!-- Welcome Section -->
            <div class="welcome-section">
                <div class="row align-items-center">
                    <div class="col-md-8">
                        <h1 class="display-5 fw-bold text-primary">
                            <i class="fas fa-tachometer-alt me-3"></i>🎯 Your Career Analysis Dashboard
                        </h1>
                        <p class="lead">🧠 <strong>AI Analysis Complete!</strong> Here are your personalized career recommendations based on your profile.</p>
                        <div class="alert alert-info">
                            <i class="fas fa-info-circle me-2"></i>
                            <strong>Authentication Required:</strong> This dashboard shows results after login and profile setup. 
                            <a href="/profile" class="alert-link">Update Profile</a> | 
                            <a href="/login" class="alert-link">Login</a>
                        </div>
                    </div>
                    <div class="col-md-4 text-center">
                        <div class="brain-icon" style="font-size: 4rem; color: #667eea; animation: pulse 2s infinite;">
                            <i class="fas fa-chart-line"></i>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Stats Cards -->
            <div class="row mb-4">
                <div class="col-md-3 mb-3">
                    <div class="card stat-card">
                        <div class="card-body text-center">
                            <i class="fas fa-file-alt fa-2x mb-2"></i>
                            <h3 class="mb-0">1</h3>
                            <p class="mb-0">Resumes Analyzed</p>
                        </div>
                    </div>
                </div>
                <div class="col-md-3 mb-3">
                    <div class="card stat-card">
                        <div class="card-body text-center">
                            <i class="fas fa-star fa-2x mb-2"></i>
                            <h3 class="mb-0">5</h3>
                            <p class="mb-0">Recommendations</p>
                        </div>
                    </div>
                </div>
                <div class="col-md-3 mb-3">
                    <div class="card stat-card">
                        <div class="card-body text-center">
                            <i class="fas fa-graduation-cap fa-2x mb-2"></i>
                            <h3 class="mb-0">12</h3>
                            <p class="mb-0">Skills Identified</p>
                        </div>
                    </div>
                </div>
                <div class="col-md-3 mb-3">
                    <div class="card stat-card">
                        <div class="card-body text-center">
                            <i class="fas fa-percent fa-2x mb-2"></i>
                            <h3 class="mb-0">85%</h3>
                            <p class="mb-0">Profile Match</p>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Action Cards -->
            <div class="row">
                <div class="col-md-6 mb-4">
                    <div class="card h-100">
                        <div class="card-body text-center">
                            <i class="fas fa-upload fa-3x text-primary mb-3"></i>
                            <h5>Upload Resume</h5>
                            <p class="text-muted">Upload your resume for AI-powered analysis and career recommendations.</p>
                            <button class="btn btn-primary" onclick="uploadResume()">
                                <i class="fas fa-cloud-upload-alt me-2"></i>Upload Now
                            </button>
                        </div>
                    </div>
                </div>
                <div class="col-md-6 mb-4">
                    <div class="card h-100">
                        <div class="card-body text-center">
                            <i class="fas fa-compass fa-3x text-success mb-3"></i>
                            <h5>Explore Careers</h5>
                            <p class="text-muted">Discover new career paths based on your skills and interests.</p>
                            <button class="btn btn-success" onclick="exploreCareers()">
                                <i class="fas fa-search me-2"></i>Explore Now
                            </button>
                        </div>
                    </div>
                </div>
                <div class="col-md-6 mb-4">
                    <div class="card h-100">
                        <div class="card-body text-center">
                            <i class="fas fa-brain fa-3x text-warning mb-3"></i>
                            <h5>Skills Assessment</h5>
                            <p class="text-muted">Take our comprehensive skills assessment for better recommendations.</p>
                            <button class="btn btn-warning" onclick="takeAssessment()">
                                <i class="fas fa-clipboard-check me-2"></i>Start Assessment
                            </button>
                        </div>
                    </div>
                </div>
                <div class="col-md-6 mb-4">
                    <div class="card h-100">
                        <div class="card-body text-center">
                            <i class="fas fa-chart-line fa-3x text-info mb-3"></i>
                            <h5>Progress Report</h5>
                            <p class="text-muted">View detailed analytics and progress tracking for your career journey.</p>
                            <button class="btn btn-info" onclick="viewReport()">
                                <i class="fas fa-chart-bar me-2"></i>View Report
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
        <script>
            function uploadResume() {
                alert('Resume upload functionality coming soon!');
            }
            function exploreCareers() {
                alert('Career exploration feature coming soon!');
            }
            function takeAssessment() {
                alert('Skills assessment feature coming soon!');
            }
            function viewReport() {
                alert('Progress report feature coming soon!');
            }
            
            // Add some animations
            document.addEventListener('DOMContentLoaded', function() {
                const cards = document.querySelectorAll('.card');
                cards.forEach((card, index) => {
                    card.style.animation = `fadeInUp 0.8s ease ${index * 0.1}s both`;
                });
            });
            
            // CSS animations
            const style = document.createElement('style');
            style.textContent = `
                @keyframes fadeInUp {
                    from { opacity: 0; transform: translateY(20px); }
                    to { opacity: 1; transform: translateY(0); }
                }
                @keyframes pulse {
                    0%, 100% { transform: scale(1); }
                    50% { transform: scale(1.05); }
                }
            `;
            document.head.appendChild(style);
        </script>
    </body>
    </html>
    '''

@app.route('/profile')
def profile():
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>📋 Setup Profile - CareerAI</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; font-family: 'Inter', sans-serif; }
            .container { padding: 2rem 1rem; }
            .profile-card { background: white; border-radius: 20px; padding: 3rem; box-shadow: 0 20px 50px rgba(0,0,0,0.1); max-width: 800px; margin: 0 auto; }
            .header { text-align: center; margin-bottom: 3rem; }
            .brain-icon { font-size: 3rem; color: #667eea; margin-bottom: 1rem; }
            .title { font-size: 2.5rem; font-weight: 700; color: #2c3e50; margin-bottom: 0.5rem; }
            .subtitle { color: #6c757d; font-size: 1.1rem; }
            .section-title { font-size: 1.3rem; font-weight: 600; color: #2c3e50; margin-bottom: 1rem; border-left: 4px solid #667eea; padding-left: 1rem; }
            .form-group { margin-bottom: 2rem; }
            .form-label { font-weight: 600; color: #2c3e50; margin-bottom: 0.8rem; display: block; }
            .form-control, .form-select { padding: 12px 15px; border: 2px solid #e9ecef; border-radius: 10px; font-size: 1rem; }
            .form-control:focus, .form-select:focus { border-color: #667eea; box-shadow: 0 0 0 0.2rem rgba(102, 126, 234, 0.25); }
            .skill-tags { display: flex; flex-wrap: wrap; gap: 0.5rem; margin-top: 0.5rem; }
            .skill-tag { background: #e3f2fd; color: #1976d2; padding: 0.5rem 1rem; border-radius: 20px; font-size: 0.9rem; }
            .btn-primary { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border: none; padding: 15px 40px; font-weight: 600; border-radius: 10px; font-size: 1.1rem; }
            .btn-primary:hover { transform: translateY(-2px); box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3); }
            .btn-secondary { background: rgba(108, 117, 125, 0.1); border: 2px solid #6c757d; color: #6c757d; padding: 10px 25px; border-radius: 10px; text-decoration: none; margin-right: 1rem; }
            .btn-secondary:hover { background: #6c757d; color: white; text-decoration: none; }
            .progress-bar { background: #667eea; }
            .file-upload { border: 2px dashed #667eea; border-radius: 10px; padding: 2rem; text-align: center; background: #f8f9fa; }
            .file-upload:hover { background: #e9f4ff; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="profile-card">
                <div class="header">
                    <div class="brain-icon"><i class="fas fa-user-cog"></i></div>
                    <h1 class="title">📋 Setup Your Profile</h1>
                    <p class="subtitle">Tell us about yourself to get personalized career recommendations</p>
                    <div class="progress mt-3">
                        <div class="progress-bar" role="progressbar" style="width: 25%">Step 1 of 4</div>
                    </div>
                </div>
                
                <form action="/analyze" method="POST" enctype="multipart/form-data">
                    <!-- Personal Information -->
                    <h4 class="section-title">👤 Personal Information</h4>
                    <div class="row">
                        <div class="col-md-6">
                            <div class="form-group">
                                <label class="form-label">Current Education Level</label>
                                <select class="form-select" name="education" required>
                                    <option value="">Select your level</option>
                                    <option value="high_school">High School</option>
                                    <option value="bachelor">Bachelor's Degree</option>
                                    <option value="master">Master's Degree</option>
                                    <option value="phd">PhD</option>
                                </select>
                            </div>
                        </div>
                        <div class="col-md-6">
                            <div class="form-group">
                                <label class="form-label">Years of Experience</label>
                                <select class="form-select" name="experience" required>
                                    <option value="">Select experience</option>
                                    <option value="0">Fresh Graduate (0 years)</option>
                                    <option value="1-2">1-2 years</option>
                                    <option value="3-5">3-5 years</option>
                                    <option value="6-10">6-10 years</option>
                                    <option value="10+">10+ years</option>
                                </select>
                            </div>
                        </div>
                    </div>
                    
                    <!-- Skills -->
                    <h4 class="section-title">🛠️ Your Skills</h4>
                    <div class="form-group">
                        <label class="form-label">Technical Skills (separated by commas)</label>
                        <input type="text" class="form-control" name="skills" placeholder="Python, Machine Learning, SQL, Data Analysis, etc." required>
                        <small class="text-muted">Example skills you might have</small>
                        <div class="skill-tags mt-2">
                            <span class="skill-tag">Python</span>
                            <span class="skill-tag">JavaScript</span>
                            <span class="skill-tag">SQL</span>
                            <span class="skill-tag">Machine Learning</span>
                            <span class="skill-tag">Data Analysis</span>
                        </div>
                    </div>
                    
                    <!-- Interests -->
                    <h4 class="section-title">💡 Career Interests</h4>
                    <div class="form-group">
                        <label class="form-label">What type of work interests you?</label>
                        <textarea class="form-control" name="interests" rows="3" placeholder="Describe what kind of work you enjoy, industries you're interested in, roles that excite you..." required></textarea>
                    </div>
                    
                    <!-- Resume Upload -->
                    <h4 class="section-title">📄 Upload Resume (Optional)</h4>
                    <div class="form-group">
                        <div class="file-upload">
                            <i class="fas fa-cloud-upload-alt fa-3x mb-3" style="color: #667eea;"></i>
                            <p><strong>Drag & drop your resume here</strong></p>
                            <p class="text-muted">or click to browse (PDF, DOC, DOCX)</p>
                            <input type="file" class="form-control" name="resume" accept=".pdf,.doc,.docx" style="display: none;">
                        </div>
                    </div>
                    
                    <div class="text-center mt-4">
                        <a href="/login" class="btn btn-secondary">← Back to Login</a>
                        <button type="submit" class="btn btn-primary">🧠 Start AI Analysis →</button>
                    </div>
                </form>
            </div>
        </div>
        
        <script>
            // File upload functionality
            document.querySelector('.file-upload').addEventListener('click', function() {
                document.querySelector('input[type="file"]').click();
            });
            
            document.querySelector('input[type="file"]').addEventListener('change', function() {
                if (this.files.length > 0) {
                    document.querySelector('.file-upload p').innerHTML = '<strong>✅ ' + this.files[0].name + '</strong><br><small>File selected successfully</small>';
                }
            });
        </script>
    </body>
    </html>
    '''
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Create Profile - CareerAI</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
        <style>
            body { 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                font-family: 'Inter', sans-serif;
            }
            .profile-card {
                background: rgba(255, 255, 255, 0.98);
                border-radius: 25px;
                box-shadow: 0 25px 50px rgba(0,0,0,0.15);
                backdrop-filter: blur(20px);
                margin: 2rem auto;
                max-width: 800px;
                padding: 3rem;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="profile-card">
                <div class="text-center mb-4">
                    <h1><i class="fas fa-user-plus text-primary"></i> Create Your Profile</h1>
                    <p class="text-muted">Tell us about yourself to get personalized recommendations</p>
                </div>
                
                <form>
                    <div class="row mb-3">
                        <div class="col-md-6">
                            <label class="form-label">First Name</label>
                            <input type="text" class="form-control" placeholder="Enter your first name">
                        </div>
                        <div class="col-md-6">
                            <label class="form-label">Last Name</label>
                            <input type="text" class="form-control" placeholder="Enter your last name">
                        </div>
                    </div>
                    
                    <div class="mb-3">
                        <label class="form-label">Email</label>
                        <input type="email" class="form-control" placeholder="your.email@example.com">
                    </div>
                    
                    <div class="mb-3">
                        <label class="form-label">Current Education Level</label>
                        <select class="form-select">
                            <option>Select your education level</option>
                            <option>High School</option>
                            <option>Undergraduate</option>
                            <option>Graduate</option>
                            <option>Postgraduate</option>
                        </select>
                    </div>
                    
                    <div class="mb-3">
                        <label class="form-label">Skills (comma separated)</label>
                        <textarea class="form-control" rows="3" placeholder="e.g., Python, Data Analysis, Communication, Leadership"></textarea>
                    </div>
                    
                    <div class="mb-3">
                        <label class="form-label">Career Interests</label>
                        <textarea class="form-control" rows="3" placeholder="Describe your career interests and goals"></textarea>
                    </div>
                    
                    <div class="d-grid gap-2">
                        <button type="submit" class="btn btn-primary btn-lg">Create Profile & Continue</button>
                        <a href="/" class="btn btn-outline-secondary">Back to Home</a>
                    </div>
                </form>
            </div>
        </div>
        
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    </body>
    </html>
    '''

@app.route('/logout')
def logout():
    return '''
    <script>
        alert("👋 Logged out successfully! Thank you for using CareerAI.");
        window.location.href = "/";
    </script>
    '''

@app.route('/demo')
def demo():
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Demo Dashboard - CareerAI</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
        <style>
            body { 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                font-family: 'Inter', sans-serif;
            }
            .demo-container {
                padding: 2rem;
            }
            .demo-card {
                background: rgba(255, 255, 255, 0.98);
                border-radius: 25px;
                box-shadow: 0 25px 50px rgba(0,0,0,0.15);
                backdrop-filter: blur(20px);
                padding: 2rem;
                margin-bottom: 2rem;
            }
            .demo-result {
                background: linear-gradient(135deg, #e3f2fd 0%, #f3e5f5 100%);
                border-radius: 15px;
                padding: 1.5rem;
                margin: 1rem 0;
                border-left: 4px solid #667eea;
            }
        </style>
    </head>
    <body>
        <div class="demo-container">
            <div class="demo-card">
                <h1 class="text-center mb-4">
                    <i class="fas fa-chart-line text-primary"></i> Demo Dashboard
                </h1>
                
                <div class="demo-result">
                    <h5><i class="fas fa-brain text-primary"></i> AI Analysis Result</h5>
                    <p><strong>Profile:</strong> Computer Science Student with Python & Data Analysis skills</p>
                    <p><strong>Top Recommendation:</strong> Data Scientist</p>
                    <p><strong>Match Score:</strong> 94%</p>
                    <p><strong>AI Reasoning:</strong> "Based on your Python programming skills and interest in data analysis, combined with your educational background in Computer Science, you show strong potential for a Data Scientist role. Your analytical thinking and technical skills align perfectly with industry requirements."</p>
                </div>
                
                <div class="demo-result">
                    <h5><i class="fas fa-lightbulb text-warning"></i> Alternative Recommendations</h5>
                    <ul>
                        <li><strong>Software Developer (89% match)</strong> - Strong programming foundation</li>
                        <li><strong>Business Analyst (82% match)</strong> - Analytical skills transferable</li>
                        <li><strong>ML Engineer (91% match)</strong> - Perfect blend of coding and data</li>
                    </ul>
                </div>
                
                <div class="demo-result">
                    <h5><i class="fas fa-graduation-cap text-success"></i> Skill Enhancement Suggestions</h5>
                    <ul>
                        <li>Machine Learning frameworks (TensorFlow, PyTorch)</li>
                        <li>Advanced Statistics & Mathematics</li>
                        <li>Data Visualization (Tableau, PowerBI)</li>
                        <li>SQL Database Management</li>
                    </ul>
                </div>
                
                <div class="text-center mt-4">
                    <a href="/dashboard" class="btn btn-primary me-3">Go to Real Dashboard</a>
                    <a href="/" class="btn btn-outline-secondary">Back to Home</a>
                </div>
            </div>
        </div>
        
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    </body>
    </html>
    '''
def api_test():
    return jsonify({
        'status': 'success',
        'message': 'CareerAI API is working!',
        'version': '1.0.0',
        'endpoints': [
            '/api/test',
            '/api/upload',
            '/api/analyze',
            '/api/recommend'
        ]
    })

@app.route('/api/upload', methods=['POST'])
def upload_resume():
    return jsonify({
        'status': 'success',
        'message': 'Resume upload endpoint ready',
        'note': 'File processing will be implemented here'
    })

@app.route('/api/analyze', methods=['POST'])
def analyze_profile():
    return jsonify({
        'status': 'success',
        'message': 'Profile analysis endpoint ready',
        'analysis': {
            'skills': ['Python', 'JavaScript', 'Data Analysis'],
            'experience': 'Mid-level',
            'recommendations': ['Software Developer', 'Data Analyst']
        }
    })

@app.route('/api/recommend')
def get_recommendations():
    return jsonify({
        'status': 'success',
        'recommendations': [
            {
                'title': 'Software Developer',
                'match': '95%',
                'description': 'Perfect match for your technical skills'
            },
            {
                'title': 'Data Analyst',
                'match': '88%',
                'description': 'Great fit for your analytical abilities'
            }
        ]
    })

if __name__ == '__main__':
    print("🚀 Starting CareerAI Server...")
    print("📍 Access at: http://localhost:5000")
    print("📍 Dashboard: http://localhost:5000/dashboard")
    print("📍 API Test: http://localhost:5000/api/test")
    print("-" * 50)
    
    app.run(debug=True, host='0.0.0.0', port=5000)