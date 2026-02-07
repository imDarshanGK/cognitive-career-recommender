// Wait for DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    
    // Check for hash in URL and activate appropriate tab
    function handleInitialTab() {
        const hash = window.location.hash.substring(1); // Remove the # symbol
        if (hash === 'register' || hash === 'login') {
            // Remove active class from all tabs and forms
            const tabBtns = document.querySelectorAll('.tab-btn');
            const formWrappers = document.querySelectorAll('.form-wrapper');
            
            tabBtns.forEach(tab => tab.classList.remove('active'));
            formWrappers.forEach(wrapper => wrapper.classList.remove('active'));
            
            // Activate the correct tab
            const targetTab = document.querySelector(`[data-tab="${hash}"]`);
            const targetForm = document.getElementById(hash + '-form');
            
            if (targetTab && targetForm) {
                targetTab.classList.add('active');
                targetForm.classList.add('active');
            }
        }
    }
    
    // Handle initial tab on page load
    handleInitialTab();
    
    // Tab switching functionality
    const tabBtns = document.querySelectorAll('.tab-btn');
    const formWrappers = document.querySelectorAll('.form-wrapper');
    
    tabBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const targetTab = this.getAttribute('data-tab');
            
            // Remove active class from all tabs and forms
            tabBtns.forEach(tab => tab.classList.remove('active'));
            formWrappers.forEach(wrapper => wrapper.classList.remove('active'));
            
            // Add active class to clicked tab
            this.classList.add('active');
            
            // Show corresponding form
            const targetForm = document.getElementById(targetTab + '-form');
            if (targetForm) {
                targetForm.classList.add('active');
            }
            
            // Update URL hash
            window.location.hash = targetTab;
        });
    });
    
    // Password visibility toggle
    const togglePasswordBtns = document.querySelectorAll('.toggle-password');
    
    togglePasswordBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const targetId = this.getAttribute('data-target');
            const passwordInput = document.getElementById(targetId);
            const icon = this.querySelector('i');
            
            if (passwordInput.type === 'password') {
                passwordInput.type = 'text';
                icon.classList.remove('fa-eye');
                icon.classList.add('fa-eye-slash');
            } else {
                passwordInput.type = 'password';
                icon.classList.remove('fa-eye-slash');
                icon.classList.add('fa-eye');
            }
        });
    });
    
    // Password strength indicator
    const passwordInput = document.getElementById('registerPassword');
    const strengthBar = document.querySelector('.strength-fill');
    const strengthText = document.querySelector('.strength-text');
    
    if (passwordInput) {
        passwordInput.addEventListener('input', function() {
            const password = this.value;
            const strength = calculatePasswordStrength(password);
            updatePasswordStrength(strength);
        });
    }
    
    function calculatePasswordStrength(password) {
        let score = 0;
        const checks = {
            length: password.length >= 8,
            lowercase: /[a-z]/.test(password),
            uppercase: /[A-Z]/.test(password),
            numbers: /\d/.test(password),
            special: /[!@#$%^&*(),.?":{}|<>]/.test(password)
        };
        
        score = Object.values(checks).filter(Boolean).length;
        
        return {
            score: score,
            percentage: (score / 5) * 100,
            text: getStrengthText(score)
        };
    }
    
    function getStrengthText(score) {
        const strengthLevels = ['Very Weak', 'Weak', 'Fair', 'Good', 'Strong'];
        return strengthLevels[score] || 'Very Weak';
    }
    
    function updatePasswordStrength(strength) {
        if (strengthBar && strengthText) {
            strengthBar.style.width = strength.percentage + '%';
            strengthText.textContent = strength.text;
            
            // Update color based on strength
            const colors = ['#ef4444', '#f97316', '#eab308', '#22c55e', '#16a34a'];
            strengthBar.style.background = colors[strength.score] || '#ef4444';
        }
    }
    
    // Form validation
    function validateEmail(email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    }
    
    function validatePassword(password) {
        return password.length >= 8;
    }
    
    function validateName(name) {
        return name.length >= 2;
    }
    
    function showError(fieldId, message) {
        const errorElement = document.getElementById(fieldId + 'Error');
        if (errorElement) {
            errorElement.textContent = message;
            errorElement.style.display = 'block';
        }
    }
    
    function clearError(fieldId) {
        const errorElement = document.getElementById(fieldId + 'Error');
        if (errorElement) {
            errorElement.textContent = '';
            errorElement.style.display = 'none';
        }
    }
    
    function clearAllErrors() {
        const errorElements = document.querySelectorAll('.error-message');
        errorElements.forEach(element => {
            element.textContent = '';
            element.style.display = 'none';
        });
    }
    
    // Login form submission
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            clearAllErrors();
            
            const email = document.getElementById('loginEmail').value.trim();
            const password = document.getElementById('loginPassword').value;
            
            let isValid = true;
            
            // Validate email
            if (!email) {
                showError('loginEmail', 'Email is required');
                isValid = false;
            } else if (!validateEmail(email)) {
                showError('loginEmail', 'Please enter a valid email address');
                isValid = false;
            }
            
            // Validate password
            if (!password) {
                showError('loginPassword', 'Password is required');
                isValid = false;
            }
            
            if (isValid) {
                const submitBtn = this.querySelector('button[type="submit"]');
                simulateFormSubmission(submitBtn, 'Signing in...', () => {
                    alert('Login successful! Redirecting to dashboard...');
                    // Here you would typically redirect to the main app
                    console.log('Login data:', { email, password });
                });
            }
        });
    }
    
    // Register form submission
    const registerForm = document.getElementById('registerForm');
    if (registerForm) {
        registerForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            clearAllErrors();
            
            const name = document.getElementById('registerName').value.trim();
            const email = document.getElementById('registerEmail').value.trim();
            const password = document.getElementById('registerPassword').value;
            const agreeTerms = document.getElementById('agreeTerms').checked;
            
            let isValid = true;
            
            // Validate name
            if (!name) {
                showError('registerName', 'Full name is required');
                isValid = false;
            } else if (!validateName(name)) {
                showError('registerName', 'Name must be at least 2 characters long');
                isValid = false;
            }
            
            // Validate email
            if (!email) {
                showError('registerEmail', 'Email is required');
                isValid = false;
            } else if (!validateEmail(email)) {
                showError('registerEmail', 'Please enter a valid email address');
                isValid = false;
            }
            
            // Validate password
            if (!password) {
                showError('registerPassword', 'Password is required');
                isValid = false;
            } else if (!validatePassword(password)) {
                showError('registerPassword', 'Password must be at least 8 characters long');
                isValid = false;
            }
            
            // Check terms agreement
            if (!agreeTerms) {
                alert('Please agree to the Terms of Service and Privacy Policy');
                isValid = false;
            }
            
            if (isValid) {
                const submitBtn = this.querySelector('button[type="submit"]');
                simulateFormSubmission(submitBtn, 'Creating account...', () => {
                    alert('Registration successful! Welcome to CareerAI!');
                    // Here you would typically redirect to onboarding or dashboard
                    console.log('Registration data:', { name, email, password });
                });
            }
        });
    }
    
    // Continue as Guest functionality
    const guestBtn = document.getElementById('continueAsGuest');
    if (guestBtn) {
        guestBtn.addEventListener('click', function() {
            const confirmGuest = confirm('Continue as guest? You\'ll have limited access to features.');
            if (confirmGuest) {
                simulateFormSubmission(this, 'Starting guest session...', () => {
                    alert('Welcome! You\'re now browsing as a guest.');
                    // Redirect to limited dashboard or main app
                    console.log('Guest access granted');
                });
            }
        });
    }
    
    // Social login buttons
    const socialBtns = document.querySelectorAll('.social-btn');
    socialBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const provider = this.classList.contains('google-btn') ? 'Google' : 
                           this.classList.contains('linkedin-btn') ? 'LinkedIn' : 'Microsoft';
            
            simulateFormSubmission(this, `Connecting to ${provider}...`, () => {
                alert(`${provider} authentication would be handled here.`);
                console.log(`${provider} login initiated`);
            });
        });
    });
    
    // Simulate form submission with loading state
    function simulateFormSubmission(button, loadingText, onComplete) {
        const originalText = button.innerHTML;
        
        // Add loading state
        button.classList.add('loading');
        button.innerHTML = `<i class="fas fa-spinner fa-spin"></i> ${loadingText}`;
        
        // Simulate API call delay
        setTimeout(() => {
            // Remove loading state
            button.classList.remove('loading');
            button.innerHTML = originalText;
            
            // Execute completion callback
            if (onComplete) {
                onComplete();
            }
        }, 2000);
    }
    
    // Real-time input validation feedback
    const inputs = document.querySelectorAll('input[type="email"], input[type="password"], input[type="text"]');
    
    inputs.forEach(input => {
        input.addEventListener('blur', function() {
            const value = this.value.trim();
            const fieldId = this.id.replace(/^(login|register)/, '').toLowerCase();
            
            if (this.type === 'email' && value && !validateEmail(value)) {
                showError(this.id, 'Please enter a valid email address');
            } else if (this.type === 'password' && value && !validatePassword(value)) {
                showError(this.id, 'Password must be at least 8 characters long');
            } else if (this.type === 'text' && value && !validateName(value)) {
                showError(this.id, 'This field must be at least 2 characters long');
            } else {
                clearError(this.id);
            }
        });
        
        // Clear errors on input
        input.addEventListener('input', function() {
            clearError(this.id);
        });
    });
    
    // Add floating animation to shapes
    function animateShapes() {
        const shapes = document.querySelectorAll('.floating-shape');
        shapes.forEach((shape, index) => {
            const randomX = Math.random() * 100;
            const randomY = Math.random() * 100;
            const randomDelay = Math.random() * 5;
            
            shape.style.animationDelay = `${randomDelay}s`;
        });
    }
    
    // Initialize animations
    animateShapes();
    
    // Console welcome message
    console.log('🔐 Authentication System Loaded');
    console.log('Features: Login, Registration, Guest Access, Social Auth');
    console.log('Team AKATSUKI - Cognitive Career & Job Recommendation System');
});