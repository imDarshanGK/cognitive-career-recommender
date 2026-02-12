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
        <title>CareerAI - AI-Powered Career Recommendation System</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
        <style>
            :root {
                --primary: #6C63FF;
                --secondary: #00BFA6;
                --accent: #FFB703;
                --dark: #1a1a1a;
                --light: #f8f9fa;
            }
            
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body {
                font-family: 'Inter', sans-serif;
                color: var(--dark);
                background: white;
                overflow-x: hidden;
            }
            
            /* Navigation */
            nav {
                background: white;
                box-shadow: 0 2px 8px rgba(0,0,0,0.05);
                position: sticky;
                top: 0;
                z-index: 100;
            }
            
            .navbar-brand {
                font-size: 1.8rem;
                font-weight: 700;
                color: var(--primary);
            }
            
            .nav-link {
                color: var(--dark);
                font-weight: 500;
                margin: 0 1rem;
                transition: all 0.3s ease;
            }
            
            .nav-link:hover {
                color: var(--primary);
            }
            
            /* Hero Section */
            .hero-section {
                background: linear-gradient(135deg, var(--primary) 0%, #764ba2 100%);
                color: white;
                padding: 6rem 0;
                min-height: 700px;
                display: flex;
                align-items: center;
                position: relative;
                overflow: hidden;
            }
            
            .hero-section::before {
                content: '';
                position: absolute;
                width: 400px;
                height: 400px;
                background: rgba(255,255,255,0.1);
                border-radius: 50%;
                top: -100px;
                right: -100px;
            }
            
            .hero-section::after {
                content: '';
                position: absolute;
                width: 300px;
                height: 300px;
                background: rgba(255,255,255,0.05);
                border-radius: 50%;
                bottom: -50px;
                left: -50px;
            }
            
            .hero-content {
                position: relative;
                z-index: 2;
            }
            
            .hero-title {
                font-size: 3.5rem;
                font-weight: 800;
                line-height: 1.2;
                margin-bottom: 1.5rem;
                animation: fadeInUp 0.8s ease;
            }
            
            .hero-subtitle {
                font-size: 1.4rem;
                font-weight: 400;
                line-height: 1.6;
                margin-bottom: 2rem;
                opacity: 0.95;
                max-width: 600px;
                animation: fadeInUp 0.8s ease 0.2s both;
            }
            
            .hero-buttons {
                display: flex;
                gap: 1.5rem;
                margin-top: 3rem;
                animation: fadeInUp 0.8s ease 0.4s both;
            }
            
            .btn-primary-hero {
                background: var(--accent);
                color: var(--dark);
                border: none;
                padding: 18px 45px;
                font-size: 1.1rem;
                font-weight: 600;
                border-radius: 12px;
                text-decoration: none;
                transition: all 0.3s ease;
                display: inline-block;
            }
            
            .btn-primary-hero:hover {
                background: #ff9c00;
                transform: translateY(-3px);
                box-shadow: 0 15px 35px rgba(0,0,0,0.2);
                color: var(--dark);
                text-decoration: none;
            }
            
            .btn-secondary-hero {
                background: rgba(255,255,255,0.2);
                color: white;
                border: 2px solid white;
                padding: 16px 45px;
                font-size: 1.1rem;
                font-weight: 600;
                border-radius: 12px;
                text-decoration: none;
                transition: all 0.3s ease;
                display: inline-block;
                backdrop-filter: blur(10px);
            }
            
            .btn-secondary-hero:hover {
                background: white;
                color: var(--primary);
                text-decoration: none;
                transform: translateY(-3px) scale(1.02);
                box-shadow: 0 10px 25px rgba(255, 255, 255, 0.3);
            }
            
            .hero-illustration {
                text-align: center;
                animation: float 3s ease-in-out infinite;
                display: flex;
                align-items: center;
                justify-content: center;
            }
            
            .hero-illustration i {
                font-size: 18rem;
                background: linear-gradient(135deg, #FFB703 0%, #FF8800 50%, #FFB703 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                filter: drop-shadow(0 20px 40px rgba(255, 183, 3, 0.3));
                transition: all 0.5s ease;
            }
            
            .hero-illustration i:hover {
                filter: drop-shadow(0 25px 50px rgba(255, 183, 3, 0.5));
                transform: scale(1.05);
            }
                filter: drop-shadow(0 10px 30px rgba(0,0,0,0.1));
            }
            
            /* Features Section */
            .features-section {
                padding: 8rem 0;
                background: var(--light);
            }
            
            .section-title {
                font-size: 3rem;
                font-weight: 800;
                text-align: center;
                margin-bottom: 1rem;
                color: var(--dark);
            }
            
            .section-subtitle {
                text-align: center;
                color: #6c757d;
                font-size: 1.2rem;
                margin-bottom: 4rem;
                max-width: 600px;
                margin-left: auto;
                margin-right: auto;
            }
            
            .feature-card {
                background: white;
                border-radius: 20px;
                padding: 2.5rem;
                text-align: center;
                transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
                box-shadow: 0 5px 20px rgba(0,0,0,0.05);
                margin-bottom: 2rem;
                display: flex;
                flex-direction: column;
                height: 100%;
                min-height: 400px;
                border: 2px solid transparent;
            }
            
            .feature-card:hover {
                transform: translateY(-10px);
                box-shadow: 0 20px 50px rgba(108, 99, 255, 0.15);
                border-color: var(--primary);
            }
            
            .feature-card:hover .feature-icon {
                animation: pulse 1s ease-in-out;
            }
            
            .feature-icon {
                font-size: 3rem;
                margin-bottom: 1.5rem;
                background: linear-gradient(135deg, var(--primary), var(--secondary));
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
            }
            
            .feature-title {
                font-size: 1.5rem;
                font-weight: 700;
                margin-bottom: 1rem;
                color: var(--dark);
            }
            
            .feature-text {
                color: #6c757d;
                font-size: 1rem;
                line-height: 1.6;
                flex-grow: 1;
            }
            
            /* How It Works */
            .workflow-section {
                padding: 8rem 0;
                background: white;
            }
            
            .workflow-container {
                max-width: 1000px;
                margin: 0 auto;
            }
            
            .workflow-steps {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
                gap: 1rem;
                margin-top: 4rem;
                position: relative;
                padding: 0;
                justify-items: center;
            }
            
            .workflow-steps::before {
                content: '';
                position: absolute;
                top: 40px;
                left: 0;
                right: 0;
                height: 3px;
                background: linear-gradient(90deg, var(--primary), var(--secondary), var(--accent));
                z-index: 0;
            }
            
            .workflow-step {
                text-align: center;
                position: relative;
                z-index: 1;
                transition: all 0.3s ease;
            }
            
            .workflow-step:hover {
                transform: scale(1.08);
            }
            
            .step-number {
                width: 90px;
                height: 90px;
                background: linear-gradient(135deg, var(--primary), var(--secondary));
                color: white;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 2.5rem;
                font-weight: 700;
                margin: 0 auto 1.5rem;
                box-shadow: 0 10px 30px rgba(108, 99, 255, 0.2);
                transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
                position: relative;
                border: 4px solid white;
            }
            
            .workflow-step:hover .step-number {
                transform: rotate(360deg);
                box-shadow: 0 15px 40px rgba(108, 99, 255, 0.4);
            }
            
            .step-title {
                font-weight: 600;
                font-size: 1rem;
                color: var(--dark);
                line-height: 1.4;
            }
            
            /* CTA Section */
            .cta-section {
                background: linear-gradient(135deg, var(--primary) 0%, #764ba2 100%);
                background-size: 200% 200%;
                animation: shimmer 10s ease infinite;
                color: white;
                padding: 6rem 2rem;
                text-align: center;
                margin: 4rem 0;
                border-radius: 20px;
                position: relative;
                overflow: hidden;
            }
            
            .cta-section::before {
                content: '';
                position: absolute;
                top: -50%;
                left: -50%;
                width: 200%;
                height: 200%;
                background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
                animation: float 6s ease-in-out infinite;
            }
            
            .cta-title {
                font-size: 2.5rem;
                font-weight: 800;
                margin-bottom: 2rem;
                position: relative;
                z-index: 1;
            }
            
            .cta-urgency {
                display: inline-block;
                background: rgba(255, 183, 3, 0.2);
                color: var(--accent);
                padding: 8px 20px;
                border-radius: 20px;
                font-weight: 600;
                margin-bottom: 1.5rem;
                font-size: 0.95rem;
                position: relative;
                z-index: 1;
            }
            
            .cta-button {
                background: var(--accent);
                color: var(--dark);
                padding: 18px 45px;
                font-size: 1.2rem;
                font-weight: 600;
                border-radius: 12px;
                text-decoration: none;
                display: inline-block;
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
                box-shadow: 0 8px 25px rgba(255, 183, 3, 0.3);
                position: relative;
                z-index: 1;
            }
            
            .cta-button:hover {
                background: #ff9c00;
                transform: translateY(-3px) scale(1.05);
                box-shadow: 0 15px 40px rgba(255, 183, 3, 0.5);
                color: var(--dark);
                text-decoration: none;
            }
                border: none;
                padding: 18px 50px;
                font-size: 1.1rem;
                font-weight: 600;
                border-radius: 12px;
                text-decoration: none;
                transition: all 0.3s ease;
                display: inline-block;
                margin-top: 1rem;
            }
            
            .cta-button:hover {
                background: #ff9c00;
                transform: translateY(-3px);
                box-shadow: 0 15px 35px rgba(0,0,0,0.2);
                color: var(--dark);
                text-decoration: none;
            }
            
            /* Footer */
            footer {
                background: var(--dark);
                color: white;
                padding: 4rem 0 2rem;
            }
            
            .footer-content {
                margin-bottom: 2rem;
            }
            
            .footer-title {
                font-weight: 700;
                margin-bottom: 1.5rem;
                color: var(--accent);
            }
            
            .footer-link {
                color: rgba(255,255,255,0.7);
                text-decoration: none;
                transition: all 0.3s ease;
                display: block;
                margin-bottom: 0.8rem;
            }
            
            .footer-link:hover {
                color: var(--accent);
            }
            
            .footer-bottom {
                border-top: 1px solid rgba(255,255,255,0.1);
                padding-top: 2rem;
                text-align: center;
                color: rgba(255,255,255,0.7);
            }
            
            /* Animations */
            @keyframes fadeInUp {
                from {
                    opacity: 0;
                    transform: translateY(30px);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }
            
            @keyframes float {
                0%, 100% {
                    transform: translateY(0px);
                }
                50% {
                    transform: translateY(-20px);
                }
            }
            
            @keyframes pulse {
                0%, 100% {
                    transform: scale(1);
                }
                50% {
                    transform: scale(1.05);
                }
            }
            
            @keyframes shimmer {
                0% {
                    background-position: -200% center;
                }
                100% {
                    background-position: 200% center;
                }
            }
            
            @keyframes countUp {
                from {
                    opacity: 0;
                    transform: translateY(20px);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }
            
            /* Responsive */
            @media (max-width: 768px) {
                .hero-title {
                    font-size: 2.5rem;
                }
                
                .hero-subtitle {
                    font-size: 1.1rem;
                }
                
                .hero-buttons {
                    flex-direction: column;
                    align-items: flex-start;
                }
                
                .btn-primary-hero,
                .btn-secondary-hero {
                    width: 100%;
                    text-align: center;
                }
                
                .hero-illustration i {
                    font-size: 12rem;
                }
                
                .section-title {
                    font-size: 2rem;
                }
                
                .workflow-steps {
                    grid-template-columns: 1fr;
                    padding: 0;
                }
                
                .workflow-steps::before {
                    display: none;
                }
                
                .cta-title {
                    font-size: 1.8rem;
                }
            }
        </style>
    </head>
    <body>
        <!-- Navigation -->
        <nav class="navbar navbar-expand-lg navbar-light">
            <div class="container-lg">
                <a class="navbar-brand" href="/">
                    <i class="fas fa-brain"></i> CareerAI
                </a>
                <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                    <span class="navbar-toggler-icon"></span>
                </button>
                <div class="collapse navbar-collapse" id="navbarNav">
                    <div class="navbar-nav ms-auto">
                        <a class="nav-link" href="#features">Features</a>
                        <a class="nav-link" href="#workflow">How It Works</a>
                        <a class="nav-link" href="/login">Login</a>
                        <a class="nav-link" href="/register" style="color: var(--primary); font-weight: 600;">Get Started</a>
                    </div>
                </div>
            </div>
        </nav>
        
        <!-- Hero Section -->
        <section class="hero-section">
            <div class="container-lg">
                <div class="row align-items-center">
                    <div class="col-lg-6 hero-content">
                        <h1 class="hero-title">AI-Powered Career Recommendations</h1>
                        <p class="hero-subtitle">A cognitive AI system that analyzes your profile, identifies career matches, and provides explainable reasoning for each recommendation.</p>
                        
                        <div class="hero-buttons">
                            <a href="/demo" class="btn-primary-hero">
                                <i class="fas fa-play-circle"></i> Try Demo
                            </a>
                            <a href="/login" class="btn-secondary-hero">
                                <i class="fas fa-sign-in-alt"></i> Login
                            </a>
                        </div>
                    </div>
                    
                    <div class="col-lg-6 hero-illustration">
                        <i class="fas fa-lightbulb"></i>
                    </div>
                </div>
            </div>
        </section>
        
        <!-- Problem Statement -->
        <section style="padding: 5rem 0; background: linear-gradient(to bottom, #f8f9fa, white);">
            <div class="container-lg">
                <div class="row align-items-center mb-5">
                    <div class="col-lg-6">
                        <h2 class="section-title" style="text-align: left; margin-bottom: 1.5rem;">The Challenge</h2>
                        <p style="font-size: 1.2rem; line-height: 1.8; color: #555; margin-bottom: 2rem;">
                            Many students face career confusion and uncertainty about their professional path. Traditional career counseling can be expensive and often lacks transparency in how recommendations are made.
                        </p>
                        <p style="font-size: 1.1rem; line-height: 1.7; color: #666;">
                            CareerAI uses <strong>Cognitive Intelligence</strong> to analyze profiles like a career counselor and <strong>Explainable AI (XAI)</strong> to show exactly why each recommendation is made.
                        </p>
                    </div>
                    <div class="col-lg-6">
                        <div class="row text-center">
                            <div class="col-6 mb-4">
                                <div style="background: white; padding: 2rem; border-radius: 15px; box-shadow: 0 5px 20px rgba(0,0,0,0.08); animation: countUp 1s ease;">
                                    <div style="font-size: 2.5rem; font-weight: 800; color: var(--primary); margin-bottom: 0.5rem;"><i class="fas fa-brain"></i></div>
                                    <p style="color: #666; font-weight: 600;">Cognitive AI Analysis</p>
                                </div>
                            </div>
                            <div class="col-6 mb-4">
                                <div style="background: white; padding: 2rem; border-radius: 15px; box-shadow: 0 5px 20px rgba(0,0,0,0.08); animation: countUp 1s ease 0.2s both;">
                                    <div style="font-size: 2.5rem; font-weight: 800; color: var(--secondary); margin-bottom: 0.5rem;"><i class="fas fa-eye"></i></div>
                                    <p style="color: #666; font-weight: 600;">Explainable Reasoning</p>
                                </div>
                            </div>
                            <div class="col-6">
                                <div style="background: white; padding: 2rem; border-radius: 15px; box-shadow: 0 5px 20px rgba(0,0,0,0.08); animation: countUp 1s ease 0.4s both;">
                                    <div style="font-size: 2.5rem; font-weight: 800; color: var(--accent); margin-bottom: 0.5rem;"><i class="fas fa-road"></i></div>
                                    <p style="color: #666; font-weight: 600;">Learning Roadmap</p>
                                </div>
                            </div>
                            <div class="col-6">
                                <div style="background: white; padding: 2rem; border-radius: 15px; box-shadow: 0 5px 20px rgba(0,0,0,0.08); animation: countUp 1s ease 0.6s both;">
                                    <div style="font-size: 2.5rem; font-weight: 800; color: #e74c3c; margin-bottom: 0.5rem;"><i class="fas fa-chart-gap"></i></div>
                                    <p style="color: #666; font-weight: 600;">Skill Gap Analysis</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section>
        
        <!-- Features Section -->
        <section class="features-section" id="features">
            <div class="container-lg">
                <h2 class="section-title">Cognitive AI Features</h2>
                <p class="section-subtitle">Two core pillars that power intelligent career recommendations</p>
                
                <div class="row justify-content-center">
                    <div class="col-lg-5 col-md-6 mb-4">
                        <div class="feature-card">
                            <div class="feature-icon">
                                <i class="fas fa-brain"></i>
                            </div>
                            <h3 class="feature-title">Cognitive Intelligence</h3>
                            <p style="font-size: 0.9rem; color: #667eea; font-weight: 600; margin: 0.5rem 0;">Thinks like a human to understand your profile deeply.</p>
                            <p class="feature-text">Advanced AI processes your skills, experience, and interests the way a career counselor would, recognizing patterns and connections beyond surface-level keywords.</p>
                        </div>
                    </div>
                    
                    <div class="col-lg-5 col-md-6 mb-4">
                        <div class="feature-card">
                            <div class="feature-icon">
                                <i class="fas fa-eye"></i>
                            </div>
                            <h3 class="feature-title">Explainable AI (XAI)</h3>
                            <p style="font-size: 0.9rem; color: #667eea; font-weight: 600; margin: 0.5rem 0;">Shows why a job is recommended with clear logic.</p>
                            <p class="feature-text">Transparency is built-in. Every recommendation comes with detailed explanations of the reasoning, so you understand exactly why CareerAI suggests each career path.</p>
                        </div>
                    </div>
                </div>
            </div>
        </section>
        
        <!-- How It Works -->
        <section class="workflow-section" id="workflow">
            <div class="container-lg workflow-container">
                <h2 class="section-title">The Cognitive Loop</h2>
                <p class="section-subtitle">7-step intelligent reasoning process</p>
                
                <div class="workflow-steps">
                    <div class="workflow-step">
                        <div class="step-number">1</div>
                        <p class="step-title">Input Profile</p>
                    </div>
                    <div class="workflow-step">
                        <div class="step-number">2</div>
                        <p class="step-title">NLP Analysis</p>
                    </div>
                    <div class="workflow-step">
                        <div class="step-number">3</div>
                        <p class="step-title">Cognitive Mapping</p>
                    </div>
                    <div class="workflow-step">
                        <div class="step-number">4</div>
                        <p class="step-title">AI Reasoning</p>
                    </div>
                    <div class="workflow-step">
                        <div class="step-number">5</div>
                        <p class="step-title">Career Match</p>
                    </div>
                    <div class="workflow-step">
                        <div class="step-number">6</div>
                        <p class="step-title">XAI Explanation</p>
                    </div>
                    <div class="workflow-step">
                        <div class="step-number">7</div>
                        <p class="step-title">Feedback Loop</p>
                    </div>
                </div>
            </div>
        </section>
        
        <!-- System Features -->
        <section style="padding: 5rem 0; background: #f8f9fa;">
            <div class="container-lg">
                <h2 class="section-title">What's Inside</h2>
                <p class="section-subtitle">Key features of the CareerAI system</p>
                <div class="row mt-5">
                    <div class="col-md-3 mb-4">
                        <div style="background: white; padding: 1.5rem; border-radius: 12px; text-align: center; box-shadow: 0 5px 15px rgba(0,0,0,0.08); transition: all 0.3s ease;" onmouseover="this.style.transform='translateY(-5px)';this.style.boxShadow='0 10px 30px rgba(108,99,255,0.15)'" onmouseout="this.style.transform='';this.style.boxShadow='0 5px 15px rgba(0,0,0,0.08)'">
                            <i class="fas fa-chart-line" style="font-size: 2.5rem; color: var(--primary); margin-bottom: 1rem;"></i>
                            <h5 style="font-weight: 600; margin-bottom: 0.5rem;">Profile Analysis</h5>
                            <p style="color: #666; font-size: 0.9rem;">Deep skill & interest insights</p>
                        </div>
                    </div>
                    <div class="col-md-3 mb-4">
                        <div style="background: white; padding: 1.5rem; border-radius: 12px; text-align: center; box-shadow: 0 5px 15px rgba(0,0,0,0.08); transition: all 0.3s ease;" onmouseover="this.style.transform='translateY(-5px)';this.style.boxShadow='0 10px 30px rgba(0,191,166,0.15)'" onmouseout="this.style.transform='';this.style.boxShadow='0 5px 15px rgba(0,0,0,0.08)'">
                            <i class="fas fa-bullseye" style="font-size: 2.5rem; color: var(--secondary); margin-bottom: 1rem;"></i>
                            <h5 style="font-weight: 600; margin-bottom: 0.5rem;">Top 3 Careers</h5>
                            <p style="color: #666; font-size: 0.9rem;">AI-matched recommendations</p>
                        </div>
                    </div>
                    <div class="col-md-3 mb-4">
                        <div style="background: white; padding: 1.5rem; border-radius: 12px; text-align: center; box-shadow: 0 5px 15px rgba(0,0,0,0.08); transition: all 0.3s ease;" onmouseover="this.style.transform='translateY(-5px)';this.style.boxShadow='0 10px 30px rgba(255,183,3,0.15)'" onmouseout="this.style.transform='';this.style.boxShadow='0 5px 15px rgba(0,0,0,0.08)'">
                            <i class="fas fa-lightbulb" style="font-size: 2.5rem; color: var(--accent); margin-bottom: 1rem;"></i>
                            <h5 style="font-weight: 600; margin-bottom: 0.5rem;">XAI Reasoning</h5>
                            <p style="color: #666; font-size: 0.9rem;">Why each career fits you</p>
                        </div>
                    </div>
                    <div class="col-md-3 mb-4">
                        <div style="background: white; padding: 1.5rem; border-radius: 12px; text-align: center; box-shadow: 0 5px 15px rgba(0,0,0,0.08); transition: all 0.3s ease;" onmouseover="this.style.transform='translateY(-5px)';this.style.boxShadow='0 10px 30px rgba(231,76,60,0.15)'" onmouseout="this.style.transform='';this.style.boxShadow='0 5px 15px rgba(0,0,0,0.08)'">
                            <i class="fas fa-road" style="font-size: 2.5rem; color: #e74c3c; margin-bottom: 1rem;"></i>
                            <h5 style="font-weight: 600; margin-bottom: 0.5rem;">Learning Roadmap</h5>
                            <p style="color: #666; font-size: 0.9rem;">Step-by-step skill path</p>
                        </div>
                    </div>
                </div>
            </div>
        </section>
        
        <!-- Footer -->
        <footer>
            <div class="container-lg">
                <div class="row mb-4">
                    <div class="col-lg-4 col-md-6 footer-content">
                        <h5 class="footer-title">CareerAI</h5>
                        <p style="color: rgba(255,255,255,0.7); font-size: 0.9rem;">AI-powered cognitive career recommendation platform.</p>
                    </div>
                    <div class="col-lg-4 col-md-6 footer-content">
                        <h5 class="footer-title">Product</h5>
                        <a href="/demo" class="footer-link">Demo</a>
                        <a href="#features" class="footer-link">Features</a>
                        <a href="#workflow" class="footer-link">Cognitive Loop</a>
                    </div>
                    <div class="col-lg-4 col-md-6 footer-content">
                        <h5 class="footer-title">Resources</h5>
                        <a href="#" class="footer-link">Documentation</a>
                        <a href="#" class="footer-link">Support</a>
                        <a href="#" class="footer-link">FAQ</a>
                    </div>
                </div>
                
                <div class="footer-bottom">
                    <p>&copy; 2026 CareerAI. All rights reserved. | Built as a Cognitive AI Project with NLP, ML & Explainable AI</p>
                </div>
            </div>
        </footer>
        
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
        <title>Login - CareerAI</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
        <style>
            :root {
                --primary: #6C63FF;
                --secondary: #00BFA6;
                --accent: #FFB703;
                --dark: #1a1a1a;
            }
            
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body {
                font-family: 'Inter', sans-serif;
                background: linear-gradient(135deg, var(--primary) 0%, #764ba2 100%);
                min-height: 100vh;
                color: var(--dark);
            }
            
            .auth-container {
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
                padding: 2rem;
            }
            
            .auth-wrapper {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 0;
                border-radius: 20px;
                overflow: hidden;
                box-shadow: 0 25px 60px rgba(0,0,0,0.2);
                background: white;
                max-width: 1000px;
                width: 100%;
            }
            
            .auth-illustration {
                background: linear-gradient(135deg, var(--primary) 0%, #764ba2 100%);
                padding: 4rem 3rem;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                color: white;
            }
            
            .illustration-icon {
                font-size: 6rem;
                margin-bottom: 2rem;
                filter: drop-shadow(0 10px 30px rgba(0,0,0,0.2));
            }
            
            .illustration-text h2 {
                font-size: 2rem;
                font-weight: 700;
                margin-bottom: 1rem;
                text-align: center;
            }
            
            .illustration-text p {
                font-size: 1.1rem;
                text-align: center;
                opacity: 0.95;
                line-height: 1.6;
            }
            
            .auth-form {
                padding: 4rem 3rem;
                display: flex;
                flex-direction: column;
                justify-content: center;
            }
            
            .form-title {
                font-size: 2rem;
                font-weight: 700;
                margin-bottom: 0.5rem;
                color: var(--dark);
            }
            
            .form-subtitle {
                color: #6c757d;
                font-size: 0.95rem;
                margin-bottom: 2rem;
            }
            
            .form-group {
                margin-bottom: 1.5rem;
            }
            
            .form-label {
                display: block;
                font-weight: 600;
                color: var(--dark);
                margin-bottom: 0.6rem;
                font-size: 0.95rem;
            }
            
            .form-control {
                padding: 12px 16px;
                border: 2px solid #e0e0e0;
                border-radius: 10px;
                font-size: 1rem;
                font-family: 'Inter', sans-serif;
                transition: all 0.3s ease;
            }
            
            .form-control:focus {
                border-color: var(--primary);
                box-shadow: 0 0 0 4px rgba(108, 99, 255, 0.1);
                outline: none;
            }
            
            .btn-login {
                background: linear-gradient(135deg, var(--primary), #764ba2);
                color: white;
                border: none;
                padding: 14px 0;
                border-radius: 10px;
                font-weight: 600;
                font-size: 1rem;
                cursor: pointer;
                transition: all 0.3s ease;
                margin-top: 1rem;
            }
            
            .btn-login:hover {
                transform: translateY(-2px);
                box-shadow: 0 10px 25px rgba(108, 99, 255, 0.3);
                color: white;
            }
            
            .footer-link {
                text-align: center;
                margin-top: 1.5rem;
                color: #6c757d;
                font-size: 0.95rem;
            }
            
            .footer-link a {
                color: var(--primary);
                text-decoration: none;
                font-weight: 600;
                transition: all 0.3s ease;
            }
            
            .footer-link a:hover {
                color: #5568d3;
                text-decoration: underline;
            }
            
            @media (max-width: 768px) {
                .auth-wrapper {
                    grid-template-columns: 1fr;
                }
                
                .auth-illustration {
                    display: none;
                }
                
                .auth-form {
                    padding: 3rem 2rem;
                }
                
                .form-title {
                    font-size: 1.5rem;
                }
            }
        </style>
    </head>
    <body>
        <div class="auth-container">
            <div class="auth-wrapper">
                <!-- Left Side - Illustration -->
                <div class="auth-illustration">
                    <div class="illustration-icon">
                        <i class="fas fa-brain"></i>
                    </div>
                    <div class="illustration-text">
                        <h2>Welcome Back to CareerAI</h2>
                        <p>Continue your journey to finding the perfect career with our Cognitive AI-powered platform.</p>
                        <ul style="text-align: left; margin-top: 2rem; list-style: none; padding: 0;">
                            <li style="margin-bottom: 1rem;"><i class="fas fa-check-circle" style="color: var(--accent); margin-right: 0.5rem;"></i> Explainable AI recommendations</li>
                            <li style="margin-bottom: 1rem;"><i class="fas fa-check-circle" style="color: var(--accent); margin-right: 0.5rem;"></i> Personalized career roadmap</li>
                            <li style="margin-bottom: 1rem;"><i class="fas fa-check-circle" style="color: var(--accent); margin-right: 0.5rem;"></i> Real-time skill gap analysis</li>
                        </ul>
                    </div>
                </div>
                
                <!-- Right Side - Form -->
                <div class="auth-form">
                    <h1 class="form-title">Login</h1>
                    <p class="form-subtitle">Enter your credentials to access your account</p>
                    
                    <form action="/auth" method="POST">
                        <div class="form-group">
                            <label class="form-label"><i class="fas fa-envelope"></i> Email Address</label>
                            <input type="email" class="form-control" name="email" placeholder="you@example.com" required style="transition: all 0.3s ease;">
                        </div>
                        
                        <div class="form-group">
                            <label class="form-label"><i class="fas fa-lock"></i> Password</label>
                            <input type="password" class="form-control" name="password" placeholder="Enter your password" required style="transition: all 0.3s ease;">
                        </div>
                        
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem;">
                            <label style="display: flex; align-items: center; color: #6c757d; cursor: pointer; font-size: 0.95rem;">
                                <input type="checkbox" name="remember" style="margin-right: 0.5rem; cursor: pointer;">
                                Remember me
                            </label>
                            <a href="/forgot-password" style="color: var(--primary); text-decoration: none; font-weight: 600; font-size: 0.9rem; transition: all 0.3s ease;">Forgot Password?</a>
                        </div>
                        
                        <button type="submit" class="btn-login">
                            <i class="fas fa-sign-in-alt me-2"></i> Login
                        </button>
                    </form>
                    
                    <div class="footer-link">
                        Don't have an account? <a href="/register">Create one now</a>
                    </div>
                </div>
            </div>
        </div>
        
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
        <script>
            // Form field focus animation
            document.querySelectorAll('.form-control').forEach(input => {
                input.addEventListener('focus', function() {
                    this.style.transform = 'scale(1.01)';
                    this.style.borderColor = 'var(--primary)';
                    this.style.boxShadow = '0 0 0 3px rgba(108, 99, 255, 0.1)';
                });
                input.addEventListener('blur', function() {
                    this.style.transform = '';
                    this.style.borderColor = '';
                    this.style.boxShadow = '';
                });
            });
        </script>
    </body>
    </html>
    '''


@app.route('/register')
def register():
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Register - CareerAI</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
        <style>
            :root {
                --primary: #6C63FF;
                --secondary: #00BFA6;
                --accent: #FFB703;
                --dark: #1a1a1a;
            }
            
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body {
                font-family: 'Inter', sans-serif;
                background: linear-gradient(135deg, var(--primary) 0%, #764ba2 100%);
                min-height: 100vh;
                color: var(--dark);
            }
            
            .auth-container {
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
                padding: 2rem;
            }
            
            .auth-wrapper {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 0;
                border-radius: 20px;
                overflow: hidden;
                box-shadow: 0 25px 60px rgba(0,0,0,0.2);
                background: white;
                max-width: 1000px;
                width: 100%;
            }
            
            .auth-benefits {
                background: linear-gradient(135deg, var(--secondary) 0%, #0a8a6f 100%);
                padding: 4rem 3rem;
                display: flex;
                flex-direction: column;
                justify-content: center;
                color: white;
            }
            
            .benefits-title {
                font-size: 2rem;
                font-weight: 700;
                margin-bottom: 2rem;
            }
            
            .benefit-item {
                display: flex;
                align-items: flex-start;
                margin-bottom: 1.5rem;
            }
            
            .benefit-icon {
                font-size: 1.5rem;
                margin-right: 1rem;
                min-width: 30px;
            }
            
            .benefit-text {
                font-size: 1rem;
                line-height: 1.6;
            }
            
            .auth-form {
                padding: 4rem 3rem;
                display: flex;
                flex-direction: column;
                justify-content: center;
            }
            
            .form-title {
                font-size: 2rem;
                font-weight: 700;
                margin-bottom: 0.5rem;
                color: var(--dark);
            }
            
            .form-subtitle {
                color: #6c757d;
                font-size: 0.95rem;
                margin-bottom: 2rem;
            }
            
            .form-group {
                margin-bottom: 1rem;
            }
            
            .form-label {
                display: block;
                font-weight: 600;
                color: var(--dark);
                margin-bottom: 0.6rem;
                font-size: 0.95rem;
            }
            
            .form-control {
                padding: 12px 16px;
                border: 2px solid #e0e0e0;
                border-radius: 10px;
                font-size: 1rem;
                font-family: 'Inter', sans-serif;
                transition: all 0.3s ease;
                width: 100%;
            }
            
            .form-control:focus {
                border-color: var(--primary);
                box-shadow: 0 0 0 4px rgba(108, 99, 255, 0.1);
                outline: none;
            }
            
            .btn-register {
                background: linear-gradient(135deg, var(--primary), #764ba2);
                color: white;
                border: none;
                padding: 14px 0;
                border-radius: 10px;
                font-weight: 600;
                font-size: 1rem;
                cursor: pointer;
                transition: all 0.3s ease;
                margin-top: 1rem;
                margin-bottom: 1rem;
            }
            
            .btn-register:hover {
                transform: translateY(-2px);
                box-shadow: 0 10px 25px rgba(108, 99, 255, 0.3);
                color: white;
            }
            
            .footer-link {
                text-align: center;
                color: #6c757d;
                font-size: 0.95rem;
            }
            
            .footer-link a {
                color: var(--primary);
                text-decoration: none;
                font-weight: 600;
                transition: all 0.3s ease;
            }
            
            .footer-link a:hover {
                color: #5568d3;
                text-decoration: underline;
            }
            
            @media (max-width: 768px) {
                .auth-wrapper {
                    grid-template-columns: 1fr;
                }
                
                .auth-benefits {
                    display: none;
                }
                
                .auth-form {
                    padding: 3rem 2rem;
                }
                
                .form-title {
                    font-size: 1.5rem;
                }
            }
        </style>
    </head>
    <body>
        <div class="auth-container">
            <div class="auth-wrapper">
                <!-- Left Side - Benefits -->
                <div class="auth-benefits">
                    <div style="text-align: center; margin-bottom: 2rem;">
                        <i class="fas fa-brain" style="font-size: 4rem; margin-bottom: 1rem;"></i>
                        <h2 class="benefits-title">CareerAI System</h2>
                        <p style="opacity: 0.9; font-size: 1.1rem; margin-bottom: 0;">Cognitive AI-Powered Career Recommendation Platform</p>
                    </div>
                    
                    <div class="benefit-item">
                        <div class="benefit-icon"><i class="fas fa-brain"></i></div>
                        <div>
                            <strong style="display: block; font-size: 1.1rem; margin-bottom: 0.3rem;">Cognitive Intelligence</strong>
                            <div class="benefit-text">AI thinks like a career counselor to understand you deeply</div>
                        </div>
                    </div>
                    
                    <div class="benefit-item">
                        <div class="benefit-icon"><i class="fas fa-eye"></i></div>
                        <div>
                            <strong style="display: block; font-size: 1.1rem; margin-bottom: 0.3rem;">Explainable AI (XAI)</strong>
                            <div class="benefit-text">See WHY each career is recommended with transparent reasoning</div>
                        </div>
                    </div>
                    
                    <div class="benefit-item">
                        <div class="benefit-icon"><i class="fas fa-road"></i></div>
                        <div>
                            <strong style="display: block; font-size: 1.1rem; margin-bottom: 0.3rem;">Personalized Roadmap</strong>
                            <div class="benefit-text">Get step-by-step learning path to achieve your career</div>
                        </div>
                    </div>
                    
                    <div class="benefit-item">
                        <div class="benefit-icon"><i class="fas fa-microscope"></i></div>
                        <div>
                            <strong style="display: block; font-size: 1.1rem; margin-bottom: 0.3rem;">Skill Gap Analysis</strong>
                            <div class="benefit-text">Identify exact skills you need to bridge the gap</div>
                        </div>
                    </div>
                    
                    <div style="margin-top: 2rem; padding-top: 2rem; border-top: 1px solid rgba(255,255,255,0.2); text-align: center;">
                        <p style="font-size: 0.95rem; opacity: 0.9;"><i class="fas fa-graduation-cap"></i> Academic Project • <i class="fas fa-lock"></i> Privacy Focused • <i class="fas fa-lightbulb"></i> Explainable AI</p>
                    </div>
                </div>
                
                <!-- Right Side - Form -->
                <div class="auth-form">
                    <h1 class="form-title">Try the System</h1>
                    <p class="form-subtitle">Create an account to explore CareerAI</p>
                    
                    <form action="/register-submit" method="POST">
                        <div class="form-group">
                            <label class="form-label"><i class="fas fa-user"></i> Full Name</label>
                            <input type="text" class="form-control" name="name" placeholder="John Doe" required style="transition: all 0.3s ease;">
                        </div>
                        
                        <div class="form-group">
                            <label class="form-label"><i class="fas fa-envelope"></i> Email Address</label>
                            <input type="email" class="form-control" name="email" placeholder="you@example.com" required style="transition: all 0.3s ease;">
                        </div>
                        
                        <div class="form-group">
                            <label class="form-label"><i class="fas fa-lock"></i> Password</label>
                            <input type="password" class="form-control" name="password" placeholder="Create a strong password" required style="transition: all 0.3s ease;">
                            <small style="color: #6c757d; font-size: 0.85rem; margin-top: 0.3rem; display: block;">Minimum 8 characters</small>
                        </div>
                        
                        <button type="submit" class="btn-register">
                            <i class="fas fa-user-plus me-2"></i> Create Account
                        </button>
                    </form>
                    
                    <div class="footer-link">
                        Already have an account? <a href="/login">Login here</a>
                    </div>
                </div>
            </div>
        </div>
        
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
        <script>
            // Form field focus animation
            document.querySelectorAll('.form-control').forEach(input => {
                input.addEventListener('focus', function() {
                    this.style.transform = 'scale(1.01)';
                    this.style.borderColor = 'var(--primary)';
                    this.style.boxShadow = '0 0 0 3px rgba(108, 99, 255, 0.1)';
                });
                input.addEventListener('blur', function() {
                    this.style.transform = '';
                    this.style.borderColor = '';
                    this.style.boxShadow = '';
                });
            });
            
            // Float animation for left side
            document.querySelector('.auth-benefits').style.animation = 'float 3s ease-in-out infinite';
        </script>
    </body>
    </html>
    '''


@app.route('/demo')
def demo():
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Demo - CareerAI</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
        <style>
            :root {
                --primary: #6C63FF;
                --secondary: #00BFA6;
                --accent: #FFB703;
                --dark: #1a1a1a;
                --light: #f8f9fa;
            }
            
            body {
                font-family: 'Inter', sans-serif;
                background: linear-gradient(135deg, var(--primary) 0%, #764ba2 100%);
                min-height: 100vh;
                padding: 3rem 0;
            }
            
            .demo-container {
                max-width: 900px;
                margin: 0 auto;
                padding: 0 2rem;
            }
            
            .demo-header {
                text-align: center;
                color: white;
                margin-bottom: 3rem;
            }
            
            .demo-header h1 {
                font-size: 2.5rem;
                font-weight: 700;
                margin-bottom: 1rem;
            }
            
            .demo-header p {
                font-size: 1.1rem;
                opacity: 0.95;
            }
            
            .demo-card {
                background: white;
                border-radius: 20px;
                padding: 2.5rem;
                margin-bottom: 2rem;
                box-shadow: 0 15px 40px rgba(0,0,0,0.15);
                animation: slideIn 0.6s ease;
            }
            
            .demo-result {
                background: white;
                border-radius: 15px;
                padding: 2rem;
                margin-bottom: 1.5rem;
                border-left: 5px solid var(--primary);
            }
            
            .demo-result h5 {
                font-weight: 700;
                color: var(--dark);
                margin-bottom: 1rem;
            }
            
            .demo-result p {
                margin: 0.5rem 0;
                line-height: 1.6;
            }
            
            .demo-result ul {
                margin: 1rem 0;
                padding-left: 2rem;
            }
            
            .demo-result li {
                margin-bottom: 0.8rem;
            }
            
            .demo-score {
                display: inline-block;
                background: linear-gradient(135deg, var(--secondary), #0a8a6f);
                color: white;
                padding: 0.5rem 1rem;
                border-radius: 20px;
                font-weight: 600;
                margin: 0.5rem 0;
            }
            
            .btn-demo {
                background: linear-gradient(135deg, var(--primary), #764ba2);
                color: white;
                border: none;
                padding: 14px 40px;
                border-radius: 10px;
                font-weight: 600;
                text-decoration: none;
                transition: all 0.3s ease;
                display: inline-block;
                margin: 0.5rem;
            }
            
            .btn-demo:hover {
                transform: translateY(-2px);
                box-shadow: 0 10px 25px rgba(108, 99, 255, 0.3);
                color: white;
                text-decoration: none;
            }
            
            @keyframes slideIn {
                from {
                    opacity: 0;
                    transform: translateY(20px);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }
        </style>
    </head>
    <body>
        <div class="demo-container">
            <div class="demo-header">
                <h1><i class="fas fa-microscope"></i> CareerAI Demo</h1>
                <p>See how our Cognitive AI recommends careers with explainable reasoning</p>
            </div>
            
            <div class="demo-card">
                <div class="demo-result">
                    <h5><i class="fas fa-user-graduate"></i> Sample Profile</h5>
                    <p><strong>Education:</strong> Bachelor's in Computer Science</p>
                    <p><strong>Experience:</strong> 2 years as Junior Developer</p>
                    <p><strong>Technical Skills:</strong> Python, JavaScript, SQL, Machine Learning, Data Analysis</p>
                    <p><strong>Interests:</strong> Problem-solving, Building intelligent systems, Working with data</p>
                </div>
                
                <div class="demo-result" style="border-left-color: var(--accent);">
                    <h5><i class="fas fa-star"></i> Top Recommendation</h5>
                    <p><strong>Role: Machine Learning Engineer</strong></p>
                    <p class="demo-score">94% Match Score</p>
                    <p><strong>AI Reasoning:</strong> "Based on your strong foundation in Python, demonstrated interest in machine learning, and analytical thinking skills, you are excellently positioned for a Machine Learning Engineer role. Your experience with data analysis and programming fundamentals directly align with industry requirements. Your stated interest in building intelligent systems perfectly matches this career path."</p>
                </div>
                
                <div class="demo-result" style="border-left-color: var(--secondary);">
                    <h5><i class="fas fa-lightbulb"></i> Alternative Recommendations</h5>
                    <ul>
                        <li><strong>Data Scientist (89% match)</strong> - Your data analysis and statistical thinking skills are exceptional</li>
                        <li><strong>Full Stack Developer (85% match)</strong> - Solid programming foundation across multiple languages</li>
                        <li><strong>Solutions Architect (82% match)</strong> - Technical depth combined with problem-solving ability</li>
                    </ul>
                </div>
                
                <div class="demo-result" style="border-left-color: #ff6b6b;">
                    <h5><i class="fas fa-graduation-cap"></i> Growth Recommendations</h5>
                    <ul>
                        <li>Deep Learning: TensorFlow, PyTorch frameworks</li>
                        <li>Advanced Mathematics: Linear Algebra, Probability & Statistics</li>
                        <li>Data Engineering: Spark, Hadoop ecosystem</li>
                        <li>Cloud Platforms: AWS/GCP ML services</li>
                    </ul>
                </div>
            </div>
            
            <div style="text-align: center;">
                <a href="/register" class="btn-demo">
                    <i class="fas fa-rocket"></i> Get Your Analysis
                </a>
                <a href="/" class="btn-demo" style="background: rgba(255,255,255,0.2); border: 2px solid white; color: white;">
                    <i class="fas fa-arrow-left"></i> Back to Home
                </a>
            </div>
        </div>
        
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    </body>
    </html>
    '''



@app.route('/auth', methods=['POST'])
def authenticate():
    return '''
    <!DOCTYPE html>
    <html>
    <head><title>Authenticating...</title></head>
    <body>
        <script>
            alert("Welcome to CareerAI! Processing your login...");
            window.location.href = "/dashboard";
        </script>
    </body>
    </html>
    '''


@app.route('/register-submit', methods=['POST'])
def register_submit():
    return '''
    <!DOCTYPE html>
    <html>
    <head><title>Account Created...</title></head>
    <body>
        <script>
            alert("Account created successfully! Welcome to CareerAI!");
            window.location.href = "/dashboard";
        </script>
    </body>
    </html>
    '''


# ============ DASHBOARD NAVIGATION SIDEBAR ============
def get_sidebar():
    return '''
    <div style="width: 250px; background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%); min-height: 100vh; position: fixed; left: 0; top: 0; padding: 2rem 0; color: white; overflow-y: auto;">
        <div style="padding: 0 1.5rem; margin-bottom: 2rem; text-align: center;">
            <h3 style="color: white; margin: 0;"><i class="fas fa-brain"></i> CareerAI</h3>
        </div>
        <nav style="padding: 0;">
            <a href="/dashboard" style="display: flex; align-items: center; padding: 1rem 1.5rem; color: rgba(255,255,255,0.8); text-decoration: none; border-left: 4px solid transparent; transition: all 0.3s ease;" onmouseover="this.style.backgroundColor='rgba(255,255,255,0.1)'; this.style.borderLeftColor='#6C63FF'; this.style.color='white';" onmouseout="this.style.backgroundColor='transparent'; this.style.borderLeftColor='transparent'; this.style.color='rgba(255,255,255,0.8)';">
                <i class="fas fa-home" style="width: 20px; margin-right: 10px;"></i> Dashboard
            </a>
            <a href="/dashboard/profile" style="display: flex; align-items: center; padding: 1rem 1.5rem; color: rgba(255,255,255,0.8); text-decoration: none; border-left: 4px solid transparent; transition: all 0.3s ease;" onmouseover="this.style.backgroundColor='rgba(255,255,255,0.1)'; this.style.borderLeftColor='#6C63FF'; this.style.color='white';" onmouseout="this.style.backgroundColor='transparent'; this.style.borderLeftColor='transparent'; this.style.color='rgba(255,255,255,0.8)';">
                <i class="fas fa-user" style="width: 20px; margin-right: 10px;"></i> My Profile
            </a>
            <a href="/dashboard/analysis" style="display: flex; align-items: center; padding: 1rem 1.5rem; color: rgba(255,255,255,0.8); text-decoration: none; border-left: 4px solid transparent; transition: all 0.3s ease;" onmouseover="this.style.backgroundColor='rgba(255,255,255,0.1)'; this.style.borderLeftColor='#6C63FF'; this.style.color='white';" onmouseout="this.style.backgroundColor='transparent'; this.style.borderLeftColor='transparent'; this.style.color='rgba(255,255,255,0.8)';">
                <i class="fas fa-chart-bar" style="width: 20px; margin-right: 10px;"></i> AI Analysis
            </a>
            <a href="/dashboard/recommendations" style="display: flex; align-items: center; padding: 1rem 1.5rem; color: rgba(255,255,255,0.8); text-decoration: none; border-left: 4px solid transparent; transition: all 0.3s ease;" onmouseover="this.style.backgroundColor='rgba(255,255,255,0.1)'; this.style.borderLeftColor='#6C63FF'; this.style.color='white';" onmouseout="this.style.backgroundColor='transparent'; this.style.borderLeftColor='transparent'; this.style.color='rgba(255,255,255,0.8)';">
                <i class="fas fa-star" style="width: 20px; margin-right: 10px;"></i> Recommendations
            </a>
            <a href="/dashboard/xai" style="display: flex; align-items: center; padding: 1rem 1.5rem; color: rgba(255,255,255,0.8); text-decoration: none; border-left: 4px solid transparent; transition: all 0.3s ease;" onmouseover="this.style.backgroundColor='rgba(255,255,255,0.1)'; this.style.borderLeftColor='#6C63FF'; this.style.color='white';" onmouseout="this.style.backgroundColor='transparent'; this.style.borderLeftColor='transparent'; this.style.color='rgba(255,255,255,0.8)';">
                <i class="fas fa-lightbulb" style="width: 20px; margin-right: 10px;"></i> Explainable AI
            </a>
            <a href="/dashboard/skill-gap" style="display: flex; align-items: center; padding: 1rem 1.5rem; color: rgba(255,255,255,0.8); text-decoration: none; border-left: 4px solid transparent; transition: all 0.3s ease;" onmouseover="this.style.backgroundColor='rgba(255,255,255,0.1)'; this.style.borderLeftColor='#6C63FF'; this.style.color='white';" onmouseout="this.style.backgroundColor='transparent'; this.style.borderLeftColor='transparent'; this.style.color='rgba(255,255,255,0.8)';">
                <i class="fas fa-graduation-cap" style="width: 20px; margin-right: 10px;"></i> Skill Gap
            </a>
            <a href="/dashboard/roadmap" style="display: flex; align-items: center; padding: 1rem 1.5rem; color: rgba(255,255,255,0.8); text-decoration: none; border-left: 4px solid transparent; transition: all 0.3s ease;" onmouseover="this.style.backgroundColor='rgba(255,255,255,0.1)'; this.style.borderLeftColor='#6C63FF'; this.style.color='white';" onmouseout="this.style.backgroundColor='transparent'; this.style.borderLeftColor='transparent'; this.style.color='rgba(255,255,255,0.8)';">
                <i class="fas fa-map" style="width: 20px; margin-right: 10px;"></i> Roadmap
            </a>
            <a href="/dashboard/reports" style="display: flex; align-items: center; padding: 1rem 1.5rem; color: rgba(255,255,255,0.8); text-decoration: none; border-left: 4px solid transparent; transition: all 0.3s ease;" onmouseover="this.style.backgroundColor='rgba(255,255,255,0.1)'; this.style.borderLeftColor='#6C63FF'; this.style.color='white';" onmouseout="this.style.backgroundColor='transparent'; this.style.borderLeftColor='transparent'; this.style.color='rgba(255,255,255,0.8)';">
                <i class="fas fa-file-pdf" style="width: 20px; margin-right: 10px;"></i> Reports
            </a>
            <a href="/dashboard/settings" style="display: flex; align-items: center; padding: 1rem 1.5rem; color: rgba(255,255,255,0.8); text-decoration: none; border-left: 4px solid transparent; transition: all 0.3s ease;" onmouseover="this.style.backgroundColor='rgba(255,255,255,0.1)'; this.style.borderLeftColor='#6C63FF'; this.style.color='white';" onmouseout="this.style.backgroundColor='transparent'; this.style.borderLeftColor='transparent'; this.style.color='rgba(255,255,255,0.8)';">
                <i class="fas fa-cog" style="width: 20px; margin-right: 10px;"></i> Settings
            </a>
            <hr style="border: none; border-top: 1px solid rgba(255,255,255,0.2); margin: 1rem 0;">
            <a href="/login" style="display: flex; align-items: center; padding: 1rem 1.5rem; color: rgba(255,255,255,0.8); text-decoration: none; border-left: 4px solid transparent; transition: all 0.3s ease;" onmouseover="this.style.backgroundColor='rgba(255,255,255,0.1)'; this.style.borderLeftColor='#ff6b6b'; this.style.color='white';" onmouseout="this.style.backgroundColor='transparent'; this.style.borderLeftColor='transparent'; this.style.color='rgba(255,255,255,0.8)';">
                <i class="fas fa-sign-out-alt" style="width: 20px; margin-right: 10px;"></i> Logout
            </a>
        </nav>
    </div>
    '''

def get_dashboard_wrapper(title, content):
    return f'''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{title} - CareerAI</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
        <style>
            :root {{
                --primary: #6C63FF;
                --secondary: #00BFA6;
                --accent: #FFB703;
                --dark: #1a1a1a;
                --light: #f8f9fa;
            }}
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}
            body {{
                font-family: 'Inter', sans-serif;
                background: linear-gradient(135deg, var(--primary) 0%, #764ba2 100%);
                min-height: 100vh;
                margin: 0;
            }}
            .main-content {{
                margin-left: 250px;
                padding: 2rem;
            }}
            .page-header {{
                background: white;
                border-radius: 20px;
                padding: 2.5rem;
                margin-bottom: 2rem;
                box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            }}
            .page-header h1 {{
                color: var(--primary);
                font-size: 2.5rem;
                font-weight: 700;
                margin-bottom: 0.5rem;
            }}
            .page-header p {{
                color: #6c757d;
                font-size: 1.1rem;
            }}
            .card {{
                background: white;
                border: none;
                border-radius: 20px;
                padding: 2rem;
                box-shadow: 0 10px 30px rgba(0,0,0,0.1);
                transition: all 0.3s ease;
                margin-bottom: 2rem;
            }}
            .card:hover {{
                transform: translateY(-5px);
                box-shadow: 0 15px 40px rgba(0,0,0,0.15);
            }}
            .card-title {{
                color: var(--primary);
                font-size: 1.5rem;
                font-weight: 700;
                margin-bottom: 1rem;
            }}
            .stat-box {{
                background: linear-gradient(135deg, var(--primary), #764ba2);
                color: white;
                border-radius: 15px;
                padding: 2rem;
                text-align: center;
                margin-bottom: 1.5rem;
            }}
            .stat-value {{
                font-size: 2.5rem;
                font-weight: 700;
                margin: 0.5rem 0;
            }}
            .stat-label {{
                font-size: 0.95rem;
                opacity: 0.95;
            }}
            .btn-primary {{
                background: linear-gradient(135deg, var(--primary), #764ba2);
                border: none;
                padding: 12px 28px;
                border-radius: 10px;
                color: white;
                font-weight: 600;
                transition: all 0.3s ease;
            }}
            .btn-primary:hover {{
                transform: translateY(-2px);
                box-shadow: 0 10px 25px rgba(108, 99, 255, 0.3);
                color: white;
            }}
            .row {{
                margin-bottom: 2rem;
            }}
            @media (max-width: 768px) {{
                .main-content {{
                    margin-left: 0;
                    padding: 1rem;
                }}
                .page-header h1 {{
                    font-size: 1.8rem;
                }}
            }}
        </style>
    </head>
    <body>
        {get_sidebar()}
        <div class="main-content">
            {content}
        </div>
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    </body>
    </html>
    '''


@app.route('/dashboard')
def dashboard():
    content = '''
    <div class="page-header">
        <h1><i class="fas fa-home me-3"></i>Welcome Back, Darshan</h1>
        <p>Your personalized career intelligence dashboard powered by Cognitive AI</p>
    </div>
    
    <div class="row">
        <div class="col-lg-3 col-md-6">
            <div class="stat-box">
                <div style="font-size: 2.5rem; margin-bottom: 1rem;"><i class="fas fa-briefcase"></i></div>
                <div class="stat-value">85%</div>
                <div class="stat-label">Profile Completion</div>
            </div>
        </div>
        <div class="col-lg-3 col-md-6">
            <div class="stat-box">
                <div style="font-size: 2.5rem; margin-bottom: 1rem;"><i class="fas fa-star"></i></div>
                <div class="stat-value">Data Scientist</div>
                <div class="stat-label">Top Recommendation</div>
            </div>
        </div>
        <div class="col-lg-3 col-md-6">
            <div class="stat-box">
                <div style="font-size: 2.5rem; margin-bottom: 1rem;"><i class="fas fa-chart-bar"></i></div>
                <div class="stat-value">12</div>
                <div class="stat-label">Skills Identified</div>
            </div>
        </div>
        <div class="col-lg-3 col-md-6">
            <div class="stat-box">
                <div style="font-size: 2.5rem; margin-bottom: 1rem;"><i class="fas fa-fire"></i></div>
                <div class="stat-value">5</div>
                <div class="stat-label">Recommendations</div>
            </div>
        </div>
    </div>
    
    <div class="card">
        <h3 class="card-title"><i class="fas fa-star me-2"></i>Your Top Career Match</h3>
        <div style="border-left: 5px solid #6C63FF; padding-left: 2rem; margin-bottom: 2rem;">
            <h4 style="color: #2c3e50; margin-bottom: 0.5rem;">Data Scientist</h4>
            <p style="color: #6c757d; margin-bottom: 1rem;">An 85% match based on your skills, experience, and interests</p>
            <div style="display: flex; gap: 2rem; flex-wrap: wrap;">
                <div>
                    <strong style="color: var(--primary);">Match Score:</strong> 85%
                </div>
                <div>
                    <strong style="color: var(--secondary);">Key Skills:</strong> Python, Machine Learning, SQL
                </div>
                <div>
                    <strong style="color: var(--accent);">Demand Level:</strong> Very High
                </div>
            </div>
        </div>
        <a href="/dashboard/recommendations" class="btn btn-primary">See All Recommendations</a>
    </div>
    
    <div class="row">
        <div class="col-lg-6">
            <div class="card">
                <h3 class="card-title"><i class="fas fa-tools me-2"></i>Skills Strength</h3>
                <ul style="list-style: none; padding: 0;">
                    <li style="padding: 0.5rem 0; color: #2c3e50;"><i class="fas fa-check-circle" style="color: #00BFA6; margin-right: 0.5rem;"></i>Python - Strong</li>
                    <li style="padding: 0.5rem 0; color: #2c3e50;"><i class="fas fa-check-circle" style="color: #00BFA6; margin-right: 0.5rem;"></i>Machine Learning - Strong</li>
                    <li style="padding: 0.5rem 0; color: #2c3e50;"><i class="fas fa-check-circle" style="color: #00BFA6; margin-right: 0.5rem;"></i>SQL - Moderate</li>
                    <li style="padding: 0.5rem 0; color: #2c3e50;"><i class="fas fa-check-circle" style="color: #00BFA6; margin-right: 0.5rem;"></i>Data Analysis - Strong</li>
                </ul>
            </div>
        </div>
        <div class="col-lg-6">
            <div class="card">
                <h3 class="card-title"><i class="fas fa-warning me-2"></i>Skill Gaps</h3>
                <ul style="list-style: none; padding: 0;">
                    <li style="padding: 0.5rem 0; color: #2c3e50;"><i class="fas fa-times-circle" style="color: #ff6b6b; margin-right: 0.5rem;"></i>Deep Learning</li>
                    <li style="padding: 0.5rem 0; color: #2c3e50;"><i class="fas fa-times-circle" style="color: #ff6b6b; margin-right: 0.5rem;"></i>Advanced Statistics</li>
                    <li style="padding: 0.5rem 0; color: #2c3e50;"><i class="fas fa-times-circle" style="color: #ff6b6b; margin-right: 0.5rem;"></i>Cloud Computing (AWS/GCP)</li>
                    <li style="padding: 0.5rem 0; color: #2c3e50;"><i class="fas fa-times-circle" style="color: #ff6b6b; margin-right: 0.5rem;"></i>Data Visualization</li>
                </ul>
                <a href="/dashboard/skill-gap" class="btn btn-primary btn-sm mt-3">View Learning Path</a>
            </div>
        </div>
    </div>
    '''
    return get_dashboard_wrapper('Dashboard', content)


@app.route('/dashboard/profile')
def dashboard_profile():
    content = '''
    <div class="page-header">
        <h1><i class="fas fa-user me-3"></i>My Profile</h1>
        <p>Manage your information for accurate AI career recommendations</p>
    </div>
    
    <div class="card">
        <h3 class="card-title"><i class="fas fa-info-circle me-2"></i>Personal Information</h3>
        <div class="row">
            <div class="col-md-6 mb-3">
                <label style="font-weight: 600; color: #2c3e50;">Name</label>
                <input type="text" class="form-control" value="Darshan Kumar" style="border: 2px solid #e9ecef; border-radius: 10px; padding: 12px;">
            </div>
            <div class="col-md-6 mb-3">
                <label style="font-weight: 600; color: #2c3e50;">Email</label>
                <input type="email" class="form-control" value="darshan@example.com" style="border: 2px solid #e9ecef; border-radius: 10px; padding: 12px;">
            </div>
            <div class="col-md-6 mb-3">
                <label style="font-weight: 600; color: #2c3e50;">Education Level</label>
                <select class="form-control" style="border: 2px solid #e9ecef; border-radius: 10px; padding: 12px;">
                    <option>Bachelor's in Computer Science</option>
                    <option>Master's Degree</option>
                </select>
            </div>
            <div class="col-md-6 mb-3">
                <label style="font-weight: 600; color: #2c3e50;">Years of Experience</label>
                <select class="form-control" style="border: 2px solid #e9ecef; border-radius: 10px; padding: 12px;">
                    <option>2-3 years</option>
                </select>
            </div>
        </div>
    </div>
    
    <div class="card">
        <h3 class="card-title"><i class="fas fa-star me-2"></i>Skills</h3>
        <div class="mb-3">
            <label style="font-weight: 600; color: #2c3e50;">Technical Skills</label>
            <textarea class="form-control" style="border: 2px solid #e9ecef; border-radius: 10px; padding: 12px;" rows="3">Python, JavaScript, SQL, Machine Learning, Data Analysis</textarea>
        </div>
        <div class="mb-3">
            <label style="font-weight: 600; color: #2c3e50;">Soft Skills</label>
            <textarea class="form-control" style="border: 2px solid #e9ecef; border-radius: 10px; padding: 12px;" rows="3">Problem Solving, Communication, Leadership, Time Management</textarea>
        </div>
    </div>
    
    <div class="card">
        <h3 class="card-title"><i class="fas fa-lightbulb me-2"></i>Career Interests</h3>
        <div class="mb-3">
            <label style="font-weight: 600; color: #2c3e50;">Tell us about your career interests</label>
            <textarea class="form-control" style="border: 2px solid #e9ecef; border-radius: 10px; padding: 12px;" rows="3">I'm passionate about AI and data science. I want to work on intelligent systems that solve real-world problems. Interested in Machine Learning Engineer or Data Scientist roles.</textarea>
        </div>
        <button class="btn btn-primary"><i class="fas fa-save me-2"></i>Save Profile</button>
    </div>
    '''
    return get_dashboard_wrapper('My Profile', content)


@app.route('/dashboard/analysis')
def dashboard_analysis():
    content = '''
    <div class="page-header">
        <h1><i class="fas fa-chart-bar me-3"></i>AI Career Analysis</h1>
        <p>Deep insights into your skills, interests, and career potential</p>
    </div>
    
    <div class="card">
        <h3 class="card-title"><i class="fas fa-brain me-2"></i>Cognitive AI Analysis</h3>
        <p style="color: #6c757d; line-height: 1.8; font-size: 1.05rem;">
            Your profile shows <strong>strong analytical and technical abilities</strong> combined with genuine interest in artificial intelligence and data science. Your experience with Python, machine learning, and data analysis aligns perfectly with emerging AI roles. The cognitive reasoning analysis indicates you have the problem-solving mindset required for advanced data science positions.
        </p>
    </div>
    
    <div class="row">
        <div class="col-lg-6">
            <div class="card">
                <h3 class="card-title"><i class="fas fa-tools me-2"></i>Skills Analysis</h3>
                <div style="margin-bottom: 1.5rem;">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                        <span style="font-weight: 600; color: #2c3e50;">Python</span>
                        <span style="color: #6c757d;">85%</span>
                    </div>
                    <div style="height: 8px; background: #e9ecef; border-radius: 10px; overflow: hidden;">
                        <div style="height: 100%; width: 85%; background: linear-gradient(90deg, var(--primary), var(--secondary));"></div>
                    </div>
                </div>
                <div style="margin-bottom: 1.5rem;">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                        <span style="font-weight: 600; color: #2c3e50;">Machine Learning</span>
                        <span style="color: #6c757d;">80%</span>
                    </div>
                    <div style="height: 8px; background: #e9ecef; border-radius: 10px; overflow: hidden;">
                        <div style="height: 100%; width: 80%; background: linear-gradient(90deg, var(--primary), var(--secondary));"></div>
                    </div>
                </div>
                <div style="margin-bottom: 1.5rem;">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                        <span style="font-weight: 600; color: #2c3e50;">Data Analysis</span>
                        <span style="color: #6c757d;">75%</span>
                    </div>
                    <div style="height: 8px; background: #e9ecef; border-radius: 10px; overflow: hidden;">
                        <div style="height: 100%; width: 75%; background: linear-gradient(90deg, var(--primary), var(--secondary));"></div>
                    </div>
                </div>
            </div>
        </div>
        <div class="col-lg-6">
            <div class="card">
                <h3 class="card-title"><i class="fas fa-heart me-2"></i>Interest Domains</h3>
                <div style="display: flex; flex-wrap: wrap; gap: 0.5rem;">
                    <span style="background: linear-gradient(135deg, var(--primary), #764ba2); color: white; padding: 0.5rem 1rem; border-radius: 20px; font-size: 0.9rem;">Artificial Intelligence</span>
                    <span style="background: linear-gradient(135deg, var(--primary), #764ba2); color: white; padding: 0.5rem 1rem; border-radius: 20px; font-size: 0.9rem;">Machine Learning</span>
                    <span style="background: linear-gradient(135deg, var(--primary), #764ba2); color: white; padding: 0.5rem 1rem; border-radius: 20px; font-size: 0.9rem;">Data Science</span>
                    <span style="background: linear-gradient(135deg, var(--primary), #764ba2); color: white; padding: 0.5rem 1rem; border-radius: 20px; font-size: 0.9rem;">Problem Solving</span>
                    <span style="background: linear-gradient(135deg, var(--primary), #764ba2); color: white; padding: 0.5rem 1rem; border-radius: 20px; font-size: 0.9rem;">Research</span>
                </div>
            </div>
        </div>
    </div>
    '''
    return get_dashboard_wrapper('AI Analysis', content)


@app.route('/dashboard/recommendations')
def dashboard_recommendations():
    content = '''
    <div class="page-header">
        <h1><i class="fas fa-star me-3"></i>Career Recommendations</h1>
        <p>AI-recommended career paths based on your cognitive profile</p>
    </div>
    
    <div class="card" style="border-left: 5px solid var(--primary);">
        <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 1.5rem;">
            <div>
                <h3 style="color: var(--primary); font-size: 1.8rem; margin: 0 0 0.5rem 0;">1. Data Scientist</h3>
                <p style="color: #6c757d; margin: 0;">Analyze complex data to drive business decisions</p>
            </div>
            <div style="background: linear-gradient(135deg, var(--primary), #764ba2); color: white; padding: 1rem 1.5rem; border-radius: 15px; text-align: center;">
                <div style="font-size: 2.5rem; font-weight: 700;">85%</div>
                <div style="font-size: 0.9rem; opacity: 0.95;">Match Score</div>
            </div>
        </div>
        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; margin-bottom: 1.5rem;">
            <div>
                <strong style="color: var(--primary);">Required Skills:</strong>
                <ul style="list-style: none; padding: 0; margin-top: 0.5rem; color: #6c757d; font-size: 0.9rem;">
                    <li><i class="fas fa-check" style="color: #00BFA6; margin-right: 0.5rem;"></i>Python</li>
                    <li><i class="fas fa-check" style="color: #00BFA6; margin-right: 0.5rem;"></i>Machine Learning</li>
                    <li><i class="fas fa-times" style="color: #ff6b6b; margin-right: 0.5rem;"></i>Deep Learning</li>
                </ul>
            </div>
            <div>
                <strong style="color: var(--secondary);">Salary Range:</strong>
                <p style="margin-top: 0.5rem; color: #6c757d; font-size: 0.9rem;">₹10-20 LPA</p>
            </div>
            <div>
                <strong style="color: var(--accent);">Market Demand:</strong>
                <p style="margin-top: 0.5rem; color: #6c757d; font-size: 0.9rem;">Very High</p>
            </div>
        </div>
        <a href="/dashboard/xai" class="btn btn-primary btn-sm">Why This Career?</a>
    </div>
    
    <div class="card" style="border-left: 5px solid var(--secondary);">
        <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 1.5rem;">
            <div>
                <h3 style="color: var(--secondary); font-size: 1.8rem; margin: 0 0 0.5rem 0;">2. Machine Learning Engineer</h3>
                <p style="color: #6c757d; margin: 0;">Build and deploy intelligent systems at scale</p>
            </div>
            <div style="background: linear-gradient(135deg, var(--secondary), #0a8a6f); color: white; padding: 1rem 1.5rem; border-radius: 15px; text-align: center;">
                <div style="font-size: 2.5rem; font-weight: 700;">78%</div>
                <div style="font-size: 0.9rem; opacity: 0.95;">Match Score</div>
            </div>
        </div>
        <a href="/dashboard/xai" class="btn btn-primary btn-sm">Why This Career?</a>
    </div>
    
    <div class="card" style="border-left: 5px solid var(--accent);">
        <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 1.5rem;">
            <div>
                <h3 style="color: var(--accent); font-size: 1.8rem; margin: 0 0 0.5rem 0;">3. AI Research Scientist</h3>
                <p style="color: #6c757d; margin: 0;">Advance the frontier of artificial intelligence</p>
            </div>
            <div style="background: linear-gradient(135deg, var(--accent), #ff8c00); color: #1a1a1a; padding: 1rem 1.5rem; border-radius: 15px; text-align: center;">
                <div style="font-size: 2.5rem; font-weight: 700;">72%</div>
                <div style="font-size: 0.9rem; opacity: 0.95;">Match Score</div>
            </div>
        </div>
        <a href="/dashboard/xai" class="btn btn-primary btn-sm">Why This Career?</a>
    </div>
    '''
    return get_dashboard_wrapper('Career Recommendations', content)


@app.route('/dashboard/xai')
def dashboard_xai():
    content = '''
    <div class="page-header">
        <h1><i class="fas fa-lightbulb me-3"></i>Explainable AI (XAI)</h1>
        <p>Understanding why you're recommended for each career</p>
    </div>
    
    <div class="card">
        <h3 class="card-title"><i class="fas fa-check-circle me-2" style="color: #00BFA6;"></i>Why Data Scientist?</h3>
        
        <div style="margin-bottom: 2rem;">
            <h4 style="color: var(--primary); font-weight: 600; margin-bottom: 1rem;">Skills Matched (Green checkmarks)</h4>
            <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem;">
                <div style="background: rgba(0, 191, 166, 0.1); padding: 1rem; border-radius: 10px; border-left: 4px solid var(--secondary);">
                    <p style="margin: 0; color: #2c3e50;"><i class="fas fa-check-circle" style="color: #00BFA6; margin-right: 0.5rem;"></i><strong>Python</strong></p>
                    <small style="color: #6c757d;">Your strongest technical skill, essential for data science</small>
                </div>
                <div style="background: rgba(0, 191, 166, 0.1); padding: 1rem; border-radius: 10px; border-left: 4px solid var(--secondary);">
                    <p style="margin: 0; color: #2c3e50;"><i class="fas fa-check-circle" style="color: #00BFA6; margin-right: 0.5rem;"></i><strong>ML Knowledge</strong></p>
                    <small style="color: #6c757d;">Strong understanding of machine learning algorithms</small>
                </div>
                <div style="background: rgba(0, 191, 166, 0.1); padding: 1rem; border-radius: 10px; border-left: 4px solid var(--secondary);">
                    <p style="margin: 0; color: #2c3e50;"><i class="fas fa-check-circle" style="color: #00BFA6; margin-right: 0.5rem;"></i><strong>SQL & Databases</strong></p>
                    <small style="color: #6c757d;">Proficiency in data retrieval and management</small>
                </div>
            </div>
        </div>
        
        <div style="margin-bottom: 2rem;">
            <h4 style="color: var(--primary); font-weight: 600; margin-bottom: 1rem;">Interests Aligned</h4>
            <div style="background: linear-gradient(135deg, rgba(108, 99, 255, 0.1) 0%, rgba(0, 191, 166, 0.1) 100%); padding: 1.5rem; border-radius: 10px; border-left: 4px solid var(--primary);">
                <p style="margin: 0 0 1rem 0; color: #2c3e50;"><i class="fas fa-check-circle" style="color: var(--primary); margin-right: 0.5rem;"></i><strong>AI & Data Passion:</strong> Your stated interest in solving complex problems with data directly aligns with data science work.</p>
                <p style="margin: 0; color: #2c3e50;"><i class="fas fa-check-circle" style="color: var(--primary); margin-right: 0.5rem;"></i><strong>Problem Solving:</strong> Your analytical thinking style matches the data-driven decision-making in data science.</p>
            </div>
        </div>
        
        <div style="margin-bottom: 2rem;">
            <h4 style="color: #ff6b6b; font-weight: 600; margin-bottom: 1rem;">Skills to Develop (Red X marks)</h4>
            <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 1rem;">
                <div style="background: rgba(255, 107, 107, 0.1); padding: 1rem; border-radius: 10px; border-left: 4px solid #ff6b6b;">
                    <p style="margin: 0; color: #2c3e50;"><i class="fas fa-times-circle" style="color: #ff6b6b; margin-right: 0.5rem;"></i><strong>Deep Learning</strong></p>
                    <small style="color: #6c757d;">Advanced neural networks would enhance your profile</small>
                </div>
                <div style="background: rgba(255, 107, 107, 0.1); padding: 1rem; border-radius: 10px; border-left: 4px solid #ff6b6b;">
                    <p style="margin: 0; color: #2c3e50;"><i class="fas fa-times-circle" style="color: #ff6b6b; margin-right: 0.5rem;"></i><strong>Advanced Statistics</strong></p>
                    <small style="color: #6c757d;">Stronger statistical foundation would boost credibility</small>
                </div>
            </div>
        </div>
        
        <div style="background: linear-gradient(135deg, var(--primary), #764ba2); color: white; padding: 2rem; border-radius: 15px;">
            <h4 style="color: white; margin-top: 0;">Cognitive AI Conclusion</h4>
            <p style="margin: 0; line-height: 1.8;">Based on comprehensive analysis of your abilities, interests, and market trends, we are <strong>85% confident</strong> that a Data Scientist role would be an excellent fit for your career development. The combination of your technical foundation and genuine passion for AI creates a strong foundation for this path.</p>
        </div>
    </div>
    '''
    return get_dashboard_wrapper('Explainable AI', content)


@app.route('/dashboard/skill-gap')
def dashboard_skill_gap():
    content = '''
    <div class="page-header">
        <h1><i class="fas fa-graduation-cap me-3"></i>Skill Gap & Learning Path</h1>
        <p>Roadmap to close skill gaps for your ideal career</p>
    </div>
    
    <div class="card">
        <h3 class="card-title"><i class="fas fa-book me-2"></i>Learning Path for Data Scientist</h3>
        
        <div style="margin-bottom: 2rem;">
            <h4 style="color: var(--primary); font-weight: 600; margin-bottom: 1.5rem; border-bottom: 2px solid var(--primary); padding-bottom: 0.5rem;">Phase 1: Foundation (Months 1-2)</h4>
            <div style="background: rgba(108, 99, 255, 0.1); padding: 1.5rem; border-radius: 10px; margin-bottom: 1rem;">
                <strong style="color: var(--primary);">Advanced Statistics</strong>
                <ul style="list-style: none; padding: 0.5rem 0 0 0; color: #6c757d; font-size: 0.9rem;">
                    <li><i class="fas fa-arrow-right" style="margin-right: 0.5rem;"></i>Linear algebra, probability, hypothesis testing</li>
                    <li><i class="fas fa-arrow-right" style="margin-right: 0.5rem;"></i>Recommended: Andrew Ng's Statistics for Data Science</li>
                </ul>
            </div>
            <div style="background: rgba(108, 99, 255, 0.1); padding: 1.5rem; border-radius: 10px;">
                <strong style="color: var(--primary);">Data Visualization</strong>
                <ul style="list-style: none; padding: 0.5rem 0 0 0; color: #6c757d; font-size: 0.9rem;">
                    <li><i class="fas fa-arrow-right" style="margin-right: 0.5rem;"></i>Matplotlib, Seaborn, Tableau basics</li>
                    <li><i class="fas fa-arrow-right" style="margin-right: 0.5rem;"></i>Recommended: DataCamp's Data Visualization course</li>
                </ul>
            </div>
        </div>
        
        <div style="margin-bottom: 2rem;">
            <h4 style="color: var(--secondary); font-weight: 600; margin-bottom: 1.5rem; border-bottom: 2px solid var(--secondary); padding-bottom: 0.5rem;">Phase 2: Specialization (Months 3-5)</h4>
            <div style="background: rgba(0, 191, 166, 0.1); padding: 1.5rem; border-radius: 10px; margin-bottom: 1rem;">
                <strong style="color: var(--secondary);">Deep Learning</strong>
                <ul style="list-style: none; padding: 0.5rem 0 0 0; color: #6c757d; font-size: 0.9rem;">
                    <li><i class="fas fa-arrow-right" style="margin-right: 0.5rem;"></i>TensorFlow, PyTorch, neural networks</li>
                    <li><i class="fas fa-arrow-right" style="margin-right: 0.5rem;"></i>Recommended: Jeremy Howard's Fast.ai course</li>
                </ul>
            </div>
        </div>
        
        <div>
            <h4 style="color: var(--accent); font-weight: 600; margin-bottom: 1.5rem; border-bottom: 2px solid var(--accent); padding-bottom: 0.5rem;">Phase 3: Projects & Practice (Months 6-12)</h4>
            <div style="background: rgba(255, 183, 3, 0.1); padding: 1.5rem; border-radius: 10px;">
                <strong style="color: var(--accent);">Build Real Projects</strong>
                <ul style="list-style: none; padding: 0.5rem 0 0 0; color: #6c757d; font-size: 0.9rem;">
                    <li><i class="fas fa-arrow-right" style="margin-right: 0.5rem;"></i>Kaggle competitions to build portfolio</li>
                    <li><i class="fas fa-arrow-right" style="margin-right: 0.5rem;"></i>Real-world data analysis projects</li>
                    <li><i class="fas fa-arrow-right" style="margin-right: 0.5rem;"></i>Contribute to open-source ML projects</li>
                </ul>
            </div>
        </div>
    </div>
    '''
    return get_dashboard_wrapper('Skill Gap & Roadmap', content)


@app.route('/dashboard/roadmap')
def dashboard_roadmap():
    content = '''
    <div class="page-header">
        <h1><i class="fas fa-map me-3"></i>Career Roadmap</h1>
        <p>Your personalized timeline to career success</p>
    </div>
    
    <div style="position: relative; padding: 2rem 0;">
        <!-- Timeline vertical line -->
        <div style="position: absolute; left: 50%; transform: translateX(-50%); width: 3px; height: 100%; background: linear-gradient(180deg, var(--primary), var(--secondary)); z-index: 0;"></div>
        
        <!-- Timeline item 1 -->
        <div style="margin-bottom: 3rem; position: relative; z-index: 1;">
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 2rem;">
                <div style="text-align: right;">
                    <div class="card" style="margin-bottom: 0;">
                        <h4 style="color: var(--primary); margin-top: 0;">Short-term (0-3 months)</h4>
                        <ul style="list-style: none; padding: 0; color: #6c757d; font-size: 0.9rem;">
                            <li><i class="fas fa-check" style="color: #00BFA6; margin-right: 0.5rem;"></i>Strengthen Python skills</li>
                            <li><i class="fas fa-check" style="color: #00BFA6; margin-right: 0.5rem;"></i>Learn Statistics fundamentals</li>
                            <li><i class="fas fa-check" style="color: #00BFA6; margin-right: 0.5rem;"></i>Complete 2-3 data projects</li>
                        </ul>
                    </div>
                </div>
                <div style="display: flex; align-items: center;">
                    <div style="width: 20px; height: 20px; background: var(--primary); border: 3px solid white; border-radius: 50%; position: absolute; left: 50%; transform: translateX(-50%);" ></div>
                </div>
            </div>
        </div>
        
        <!-- Timeline item 2 -->
        <div style="margin-bottom: 3rem; position: relative; z-index: 1;">
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 2rem;">
                <div style="display: flex; align-items: center;">
                    <div style="width: 20px; height: 20px; background: var(--secondary); border: 3px solid white; border-radius: 50%; position: absolute; left: 50%; transform: translateX(-50%);"></div>
                </div>
                <div>
                    <div class="card" style="margin-bottom: 0;">
                        <h4 style="color: var(--secondary); margin-top: 0;">Mid-term (3-6 months)</h4>
                        <ul style="list-style: none; padding: 0; color: #6c757d; font-size: 0.9rem;">
                            <li><i class="fas fa-check" style="color: #00BFA6; margin-right: 0.5rem;"></i>Learn Deep Learning basics</li>
                            <li><i class="fas fa-check" style="color: #00BFA6; margin-right: 0.5rem;"></i>Master data visualization</li>
                            <li><i class="fas fa-check" style="color: #00BFA6; margin-right: 0.5rem;"></i>Start working with real datasets</li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Timeline item 3 -->
        <div style="position: relative; z-index: 1;">
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 2rem;">
                <div style="text-align: right;">
                    <div class="card" style="margin-bottom: 0;">
                        <h4 style="color: var(--accent); margin-top: 0;">Long-term (6-12 months)</h4>
                        <ul style="list-style: none; padding: 0; color: #6c757d; font-size: 0.9rem;">
                            <li><i class="fas fa-check" style="color: #00BFA6; margin-right: 0.5rem;"></i>Build impressive portfolio</li>
                            <li><i class="fas fa-check" style="color: #00BFA6; margin-right: 0.5rem;"></i>Apply for Data Scientist roles</li>
                            <li><i class="fas fa-check" style="color: #00BFA6; margin-right: 0.5rem;"></i>Secure internship or entry-level position</li>
                        </ul>
                    </div>
                </div>
                <div style="display: flex; align-items: center;">
                    <div style="width: 20px; height: 20px; background: var(--accent); border: 3px solid white; border-radius: 50%; position: absolute; left: 50%; transform: translateX(-50%);"></div>
                </div>
            </div>
        </div>
    </div>
    '''
    return get_dashboard_wrapper('Career Roadmap', content)


@app.route('/dashboard/reports')
def dashboard_reports():
    content = '''
    <div class="page-header">
        <h1><i class="fas fa-file-pdf me-3"></i>Reports & Insights</h1>
        <p>Download comprehensive analysis reports</p>
    </div>
    
    <div class="row">
        <div class="col-lg-6">
            <div class="card">
                <h3 class="card-title"><i class="fas fa-file-pdf me-2"></i>Career Recommendations Report</h3>
                <p style="color: #6c757d; margin-bottom: 1.5rem;">Comprehensive PDF with your top 5 career recommendations, match scores, and detailed analysis.</p>
                <button class="btn btn-primary"><i class="fas fa-download me-2"></i>Download PDF</button>
            </div>
        </div>
        <div class="col-lg-6">
            <div class="card">
                <h3 class="card-title"><i class="fas fa-file-pdf me-2"></i>Skills Analysis Report</h3>
                <p style="color: #6c757d; margin-bottom: 1.5rem;">Detailed breakdown of your strengths, skill gaps, and personalized learning recommendations.</p>
                <button class="btn btn-primary"><i class="fas fa-download me-2"></i>Download PDF</button>
            </div>
        </div>
        <div class="col-lg-6">
            <div class="card">
                <h3 class="card-title"><i class="fas fa-file-pdf me-2"></i>Resume Analysis Report</h3>
                <p style="color: #6c757d; margin-bottom: 1.5rem;">NLP-based analysis of your resume highlighting relevant skills and areas for improvement.</p>
                <button class="btn btn-primary"><i class="fas fa-download me-2"></i>Download PDF</button>
            </div>
        </div>
        <div class="col-lg-6">
            <div class="card">
                <h3 class="card-title"><i class="fas fa-file-pdf me-2"></i>Career Roadmap PDF</h3>
                <p style="color: #6c757d; margin-bottom: 1.5rem;">Printable timeline and actionable steps for your 12-month career development plan.</p>
                <button class="btn btn-primary"><i class="fas fa-download me-2"></i>Download PDF</button>
            </div>
        </div>
    </div>
    '''
    return get_dashboard_wrapper('Reports & Insights', content)


@app.route('/dashboard/settings')
def dashboard_settings():
    content = '''
    <div class="page-header">
        <h1><i class="fas fa-cog me-3"></i>Settings</h1>
        <p>Manage your account preferences and privacy</p>
    </div>
    
    <div class="card">
        <h3 class="card-title"><i class="fas fa-lock me-2"></i>Account Settings</h3>
        <div class="mb-3">
            <label style="font-weight: 600; color: #2c3e50;">Current Password</label>
            <input type="password" class="form-control" placeholder="Enter current password" style="border: 2px solid #e9ecef; border-radius: 10px; padding: 12px;">
        </div>
        <div class="mb-3">
            <label style="font-weight: 600; color: #2c3e50;">New Password</label>
            <input type="password" class="form-control" placeholder="Enter new password" style="border: 2px solid #e9ecef; border-radius: 10px; padding: 12px;">
        </div>
        <div class="mb-3">
            <label style="font-weight: 600; color: #2c3e50;">Confirm Password</label>
            <input type="password" class="form-control" placeholder="Confirm new password" style="border: 2px solid #e9ecef; border-radius: 10px; padding: 12px;">
        </div>
        <button class="btn btn-primary"><i class="fas fa-save me-2"></i>Change Password</button>
    </div>
    
    <div class="card">
        <h3 class="card-title"><i class="fas fa-shield-alt me-2"></i>Privacy & Data</h3>
        <div style="margin-bottom: 1.5rem;">
            <label style="display: flex; align-items: center; cursor: pointer; color: #2c3e50;">
                <input type="checkbox" style="margin-right: 1rem; width: 20px; height: 20px; cursor: pointer;" checked>
                Allow CareerAI to analyze my profile for recommendations
            </label>
        </div>
        <div style="margin-bottom: 1.5rem;">
            <label style="display: flex; align-items: center; cursor: pointer; color: #2c3e50;">
                <input type="checkbox" style="margin-right: 1rem; width: 20px; height: 20px; cursor: pointer;" checked>
                Share anonymous insights with research community
            </label>
        </div>
        <div style="margin-bottom: 1.5rem;">
            <label style="display: flex; align-items: center; cursor: pointer; color: #2c3e50;">
                <input type="checkbox" style="margin-right: 1rem; width: 20px; height: 20px; cursor: pointer;">
                Receive email notifications about job recommendations
            </label>
        </div>
        <button class="btn btn-primary btn-sm"><i class="fas fa-save me-2"></i>Save Preferences</button>
    </div>
    
    <div class="card">
        <h3 class="card-title"><i class="fas fa-trash me-2" style="color: #ff6b6b;"></i>Danger Zone</h3>
        <p style="color: #6c757d; margin-bottom: 1.5rem;">Delete your account and all associated data permanently.</p>
        <button class="btn" style="background: #ff6b6b; color: white; border: none; padding: 12px 28px; border-radius: 10px; font-weight: 600; cursor: pointer; transition: all 0.3s ease;" onmouseover="this.style.background='#ff5252';" onmouseout="this.style.background='#ff6b6b';"><i class="fas fa-trash me-2"></i>Delete Account</button>
    </div>
    '''
    return get_dashboard_wrapper('Settings', content)


@app.route('/api/test')
def api_test():
    return jsonify({
        'status': 'success',
        'message': 'CareerAI API is running',
        'version': '2.0',
    })


if __name__ == '__main__':
    print("\n" + "="*60)
    print("  CareerAI - Cognitive Career Recommendation System")
    print("="*60)
    print("\nServer starting on http://localhost:5000")
    print("\nAvailable routes:")
    print("  Home        ➜ http://localhost:5000/")
    print("  Login       ➜ http://localhost:5000/login")
    print("  Register    ➜ http://localhost:5000/register")
    print("  Demo        ➜ http://localhost:5000/demo")
    print("  Dashboard   ➜ http://localhost:5000/dashboard")
    print("\n" + "="*60 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
