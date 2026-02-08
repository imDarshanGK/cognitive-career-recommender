// Wait for DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 Script loaded successfully!');
    
    try {
        // Get button elements with error checking
        const getStartedBtn = document.getElementById('getStartedBtn');
        const loginBtn = document.getElementById('loginBtn');
        const tryDemoBtn = document.getElementById('tryDemoBtn');
        
        console.log('Button search results:', {
            getStarted: !!getStartedBtn,
            login: !!loginBtn,
            tryDemo: !!tryDemoBtn
        });
        
        // Get Started Button Functionality
        if (getStartedBtn) {
            console.log('Get Started button found, adding event listener');
            getStartedBtn.addEventListener('click', function() {
                console.log('Get Started button clicked - navigating to auth.html#register');
                window.location.href = 'auth.html#register';
            });
        } else {
            console.error('Get Started button not found!');
        }
        
        // Login Button Functionality
        if (loginBtn) {
            console.log('Login button found, adding event listener');
            loginBtn.addEventListener('click', function() {
                console.log('Login button clicked - navigating to auth.html#login');
                window.location.href = 'auth.html#login';
            });
        } else {
            console.error('Login button not found!');
        }
        
        // Try Demo Button Functionality
        if (tryDemoBtn) {
            console.log('Try Demo button found, adding event listener');
            tryDemoBtn.addEventListener('click', function() {
                console.log('Try Demo button clicked - showing demo');
                alert('🧠 AI Demo: Career Match - Data Scientist (96% match)\n📈 Missing Skills: ML, SQL\n\nSign up to get your full career analysis!');
            });
        } else {
            console.error('Try Demo button not found!');
        }
    
        // Add smooth scrolling for any anchor links
        try {
            const anchorLinks = document.querySelectorAll('a[href^="#"]');
            anchorLinks.forEach(anchor => {
                anchor.addEventListener('click', function (e) {
                    try {
                        e.preventDefault();
                        const targetId = this.getAttribute('href');
                        const targetElement = document.querySelector(targetId);
                        
                        if (targetElement) {
                            targetElement.scrollIntoView({
                                behavior: 'smooth',
                                block: 'start'
                            });
                        }
                    } catch (scrollError) {
                        console.error('Error in smooth scrolling:', scrollError);
                    }
                });
            });
        } catch (error) {
            console.warn('Smooth scrolling setup failed:', error);
        }
    
        // Add fade-in animation for feature cards on scroll
        try {
            const observerOptions = {
                threshold: 0.1,
                rootMargin: '0px 0px -50px 0px'
            };
            
            if ('IntersectionObserver' in window) {
                const observer = new IntersectionObserver(function(entries) {
                    entries.forEach(entry => {
                        try {
                            if (entry.isIntersecting) {
                                entry.target.style.opacity = '1';
                                entry.target.style.transform = 'translateY(0)';
                                observer.unobserve(entry.target);
                            }
                        } catch (observerError) {
                            console.error('Error in intersection observer:', observerError);
                        }
                    });
                }, observerOptions);
                
                // Observe feature cards and thinking steps
                const animatedElements = document.querySelectorAll('.feature-card, .thinking-step');
                animatedElements.forEach(el => {
                    if (el) {
                        el.style.opacity = '0';
                        el.style.transform = 'translateY(20px)';
                        el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
                        observer.observe(el);
                    }
                });
            } else {
                // Fallback for browsers without IntersectionObserver
                const animatedElements = document.querySelectorAll('.feature-card, .thinking-step');
                animatedElements.forEach(el => {
                    if (el) {
                        el.style.opacity = '1';
                        el.style.transform = 'translateY(0)';
                    }
                });
            }
        } catch (error) {
            console.warn('Animation setup failed:', error);
        }
        
    } catch (error) {
        console.error('Main script initialization failed:', error);
    }
});

// Demo Modal Functionality
function showDemoModal() {
    try {
        // Create demo modal
        const modal = document.createElement('div');
        modal.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.8);
            display: flex;
            justify-content: center;
            align-items: center;
            z-index: 10000;
            opacity: 0;
            transition: opacity 0.3s ease;
        `;
        
        const modalContent = document.createElement('div');
        modalContent.style.cssText = `
            background: white;
            padding: 2rem;
            border-radius: 15px;
            max-width: 500px;
            max-height: 80vh;
            overflow-y: auto;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            text-align: center;
            transform: scale(0.8);
            transition: transform 0.3s ease;
        `;
        
        modalContent.innerHTML = `
            <h2 style="color: #6C63FF; margin-bottom: 1rem;">🧠 AI Demo Experience</h2>
            <p style="color: #6b7280; margin-bottom: 1.5rem;">Experience our AI-powered career recommendations:</p>
            <div style="text-align: left; margin: 1.5rem 0;">
                <div style="padding: 1rem; background: #f8fafc; border-radius: 8px; margin-bottom: 1rem;">
                    <strong>🎯 Career Match:</strong> Data Scientist (96% match)<br>
                    <span style="color: #6b7280; font-size: 0.9rem;">Based on your Python skills and analytical thinking</span>
                </div>
                <div style="padding: 1rem; background: #f8fafc; border-radius: 8px; margin-bottom: 1rem;">
                    <strong>📈 Skill Gaps:</strong> Machine Learning, SQL<br>
                    <span style="color: #6b7280; font-size: 0.9rem;">Recommended: Take our ML fundamentals course</span>
                </div>
            </div>
            <button id="closeDemoBtn" style="
                background: linear-gradient(45deg, #00E5A8, #00C2FF);
                color: white;
                border: none;
                padding: 0.8rem 2rem;
                border-radius: 25px;
                cursor: pointer;
                font-weight: 600;
                margin-top: 1rem;
            ">Get Full Experience</button>
        `;
        
        modal.appendChild(modalContent);
        document.body.appendChild(modal);
        
        // Animate modal in
        setTimeout(() => {
            modal.style.opacity = '1';
            modalContent.style.transform = 'scale(1)';
        }, 10);
        
        // Close modal functionality
        const closeBtn = modalContent.querySelector('#closeDemoBtn');
        const closeModal = () => {
            modal.style.opacity = '0';
            modalContent.style.transform = 'scale(0.8)';
            setTimeout(() => document.body.removeChild(modal), 300);
        };
        
        closeBtn.addEventListener('click', () => {
            closeModal();
            window.location.href = 'auth.html#register';
        });
        
        modal.addEventListener('click', (e) => {
            if (e.target === modal) closeModal();
        });
        
        // Close on Escape key
        document.addEventListener('keydown', function escHandler(e) {
            if (e.key === 'Escape') {
                closeModal();
                document.removeEventListener('keydown', escHandler);
            }
        });
        
    } catch (error) {
        console.error('Error showing demo modal:', error);
        alert('Demo: Get 96% career match as Data Scientist! Sign up to discover your perfect career path.');
    }
}

// Console message for developers
console.log('🚀 Cognitive Career & Job Recommendation System - Home Page Loaded');
console.log('Team AKATSUKI - Intelligent career guidance through Cognitive and Explainable AI');
});