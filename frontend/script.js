// Wait for DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    
    try {
        // Get button elements with error checking
        const getStartedBtn = document.getElementById('getStartedBtn');
        const loginBtn = document.getElementById('loginBtn');
        const tryDemoBtn = document.getElementById('tryDemoBtn');
        
        // Get Started Button Functionality
        if (getStartedBtn) {
            getStartedBtn.addEventListener('click', function() {
                window.location.href = 'auth.html#register';
            });
        }
        
        // Login Button Functionality
        if (loginBtn) {
            loginBtn.addEventListener('click', function() {
                window.location.href = 'auth.html#login';
            });
        }
        
        // Try Demo Button Functionality
        if (tryDemoBtn) {
            tryDemoBtn.addEventListener('click', function() {
                showDemoModal();
            });
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
                        // Silent error handling
                    }
                });
            });
        } catch (error) {
            // Silent error handling
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
                            // Silent error handling
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
            // Silent error handling
        }
        
    } catch (error) {
        // Silent error handling
    }
});

// Demo Modal Functionality
function showDemoModal() {
    try {
        // Create demo modal with improved design
        const modal = document.createElement('div');
        modal.className = 'demo-modal';
        modal.setAttribute('role', 'dialog');
        modal.setAttribute('aria-labelledby', 'demo-title');
        modal.setAttribute('aria-modal', 'true');
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
            padding: 2.5rem;
            border-radius: 20px;
            max-width: 520px;
            width: 90%;
            max-height: 80vh;
            overflow-y: auto;
            box-shadow: 0 25px 80px rgba(0, 0, 0, 0.3);
            text-align: center;
            transform: scale(0.8);
            transition: transform 0.3s ease;
        `;
        
        modalContent.innerHTML = `
            <h2 id="demo-title" style="color: #6C63FF; margin-bottom: 1.5rem; font-size: 1.8rem;">🧠 AI Career Demo</h2>
            <p style="color: #6b7280; margin-bottom: 2rem; font-size: 1.1rem;">Experience our AI-powered career recommendations:</p>
            <div style="text-align: left; margin: 2rem 0;">
                <div style="padding: 1.5rem; background: #f8fafc; border-radius: 12px; margin-bottom: 1.5rem; border-left: 4px solid #6C63FF;">
                    <strong style="color: #1f2937; font-size: 1.1rem;">🎯 Perfect Career Match</strong><br>
                    <span style="color: #4338ca; font-size: 1.2rem; font-weight: 600;">Data Scientist (96% match)</span><br>
                    <small style="color: #6b7280; font-size: 0.9rem;">Based on your analytical skills and Python expertise</small>
                </div>
                <div style="padding: 1.5rem; background: #fef3c7; border-radius: 12px; margin-bottom: 1.5rem; border-left: 4px solid #f59e0b;">
                    <strong style="color: #1f2937; font-size: 1.1rem;">📈 Skills To Develop</strong><br>
                    <span style="color: #d97706; font-weight: 600;">Machine Learning, Advanced SQL</span><br>
                    <small style="color: #6b7280; font-size: 0.9rem;">Complete these to reach 99% career readiness</small>
                </div>
                <div style="padding: 1.5rem; background: #ecfdf5; border-radius: 12px; border-left: 4px solid #10b981;">
                    <strong style="color: #1f2937; font-size: 1.1rem;">💰 Salary Potential</strong><br>
                    <span style="color: #059669; font-weight: 600; font-size: 1.2rem;">$95,000 - $140,000</span><br>
                    <small style="color: #6b7280; font-size: 0.9rem;">Average for Data Scientists in your location</small>
                </div>
            </div>
            <button id="closeDemoBtn" style="
                background: linear-gradient(45deg, #6C63FF, #7B5CFA);
                color: white;
                border: none;
                padding: 1rem 2.5rem;
                border-radius: 50px;
                cursor: pointer;
                font-weight: 600;
                font-size: 1.1rem;
                margin-top: 1.5rem;
                transition: transform 0.2s ease;
                box-shadow: 0 4px 15px rgba(108, 99, 255, 0.3);
            " onmouseover="this.style.transform='translateY(-2px)'" onmouseout="this.style.transform='translateY(0)'">
                Get My Complete Analysis
            </button>
        `;
        
        modal.appendChild(modalContent);
        document.body.appendChild(modal);
        
        // Focus management for accessibility
        const closeBtn = modalContent.querySelector('#closeDemoBtn');
        
        // Animate modal in
        setTimeout(() => {
            modal.style.opacity = '1';
            modalContent.style.transform = 'scale(1)';
            closeBtn.focus();
        }, 10);
        
        const closeModal = () => {
            modal.style.opacity = '0';
            modalContent.style.transform = 'scale(0.8)';
            setTimeout(() => {
                if (document.body.contains(modal)) {
                    document.body.removeChild(modal);
                }
            }, 300);
        };
        
        closeBtn.addEventListener('click', () => {
            closeModal();
            window.location.href = 'auth.html#register';
        });
        
        modal.addEventListener('click', (e) => {
            if (e.target === modal) closeModal();
        });
        
        // Enhanced keyboard navigation
        const handleKeydown = (e) => {
            if (e.key === 'Escape') {
                closeModal();
                document.removeEventListener('keydown', handleKeydown);
            }
            if (e.key === 'Tab') {
                e.preventDefault();
                closeBtn.focus();
            }
        };
        
        document.addEventListener('keydown', handleKeydown);
        
    } catch (error) {
        // Enhanced fallback with better messaging
        const fallbackMessage = `🧠 AI Career Demo\n\n🎯 Perfect Match: Data Scientist (96%)\n📈 Skills Needed: ML, Advanced SQL\n💰 Salary Range: $95k - $140k\n\n✨ Sign up to get your complete career analysis!`;
        alert(fallbackMessage);
    }
}
});