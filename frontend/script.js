// Wait for DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    
    // Get button elements
    const getStartedBtn = document.getElementById('getStartedBtn');
    const loginBtn = document.getElementById('loginBtn');
    
    // Get Started Button Functionality
    getStartedBtn.addEventListener('click', function() {
        // Add click animation
        this.style.transform = 'scale(0.95)';
        setTimeout(() => {
            this.style.transform = '';
            // Navigate to auth page with register tab active
            window.location.href = 'auth.html#register';
        }, 150);
    });
    
    // Login Button Functionality
    loginBtn.addEventListener('click', function() {
        // Add click animation
        this.style.transform = 'scale(0.95)';
        setTimeout(() => {
            this.style.transform = '';
            // Navigate to auth page with login tab active
            window.location.href = 'auth.html#login';
        }, 150);
    });
    
    // Add smooth scrolling for any anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            
            document.querySelector(this.getAttribute('href')).scrollIntoView({
                behavior: 'smooth'
            });
        });
    });
    
    // Add fade-in animation for feature cards on scroll
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);
    
    // Observe feature cards
    document.querySelectorAll('.feature-card').forEach(card => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(30px)';
        card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(card);
    });
    
    // Add typing effect to the title (optional enhancement)
    const title = document.querySelector('.project-title');
    const titleText = title.textContent;
    
    // Uncomment the following lines if you want a typing effect for the title
    /*
    title.textContent = '';
    title.style.borderRight = '3px solid #4ade80';
    
    let i = 0;
    function typeWriter() {
        if (i < titleText.length) {
            title.textContent += titleText.charAt(i);
            i++;
            setTimeout(typeWriter, 50);
        } else {
            title.style.borderRight = 'none';
        }
    }
    
    setTimeout(typeWriter, 1000);
    */
    
    // Console message for developers
    console.log('🚀 Cognitive Career & Job Recommendation System - Home Page Loaded');
    console.log('Team AKATSUKI - Intelligent career guidance through Cognitive and Explainable AI');
});