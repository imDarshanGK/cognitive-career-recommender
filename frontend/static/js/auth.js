/**
 * ========================================
 * AUTHENTICATION JAVASCRIPT
 * ========================================
 * Handles login, registration, and auth-related functionality
 */

'use strict';

// Authentication module
const AuthModule = {
    // Configuration
    config: {
        passwordMinLength: 8,
        emailRegex: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
        passwordRegex: {
            lowercase: /[a-z]/,
            uppercase: /[A-Z]/,
            number: /[0-9]/,
            special: /[^a-zA-Z0-9]/
        }
    },
    
    // State
    state: {
        isSubmitting: false,
        passwordVisible: false
    },
    
    // Initialize authentication module
    init: function() {
        this.setupEventListeners();
        this.initializePasswordToggles();
        this.initializeFormValidation();
    }
};

AuthModule.getCsrfToken = function() {
    return document.querySelector('meta[name="csrf-token"]')?.content || '';
};

/**
 * ========================================
 * EVENT LISTENERS SETUP
 * ========================================
 */
AuthModule.setupEventListeners = function() {
    // Login form
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', (e) => this.handleLogin(e));
    }
    
    // Registration form
    const registerForm = document.getElementById('registerForm');
    if (registerForm) {
        registerForm.addEventListener('submit', (e) => this.handleRegistration(e));

        // Real-time validation
        const emailField = registerForm.querySelector('#email');
        if (emailField) {
            emailField.addEventListener('blur', (e) => this.validateEmail(e.target));
            emailField.addEventListener('blur', (e) => this.checkEmailAvailability(e.target.value));
        }

        const passwordField = registerForm.querySelector('#password');
        if (passwordField) {
            passwordField.addEventListener('input', (e) => this.checkPasswordStrength(e.target.value));
            // Always show requirements, so no need to hide/show
        }

        const confirmPasswordField = registerForm.querySelector('#confirm_password');
        if (confirmPasswordField) {
            confirmPasswordField.addEventListener('input', () => this.validatePasswordMatch());
        }
    }
    
    // Forgot password form
    const forgotPasswordForm = document.getElementById('forgotPasswordForm');
    if (forgotPasswordForm) {
        forgotPasswordForm.addEventListener('submit', (e) => this.handleForgotPassword(e));
    }
    
    // Social login buttons
    document.querySelectorAll('[data-social-login]').forEach(button => {
        button.addEventListener('click', (e) => this.handleSocialLogin(e));
    });
};

/**
 * ========================================
 * PASSWORD TOGGLE FUNCTIONALITY
 * ========================================
 */
AuthModule.initializePasswordToggles = function() {
    document.querySelectorAll('[id^="togglePassword"]').forEach(toggle => {
        toggle.addEventListener('click', function() {
            const targetId = this.getAttribute('data-target') || 'password';
            AuthModule.togglePasswordVisibility(targetId, this);
        });
    });
    
    // Generic password toggle for any button with data-password-toggle
    document.querySelectorAll('[data-password-toggle]').forEach(toggle => {
        toggle.addEventListener('click', function() {
            const targetSelector = this.getAttribute('data-password-toggle');
            const targetField = document.querySelector(targetSelector);
            if (targetField) {
                AuthModule.togglePasswordVisibility(targetField.id, this);
            }
        });
    });
};

AuthModule.togglePasswordVisibility = function(fieldId, toggleButton) {
    const field = document.getElementById(fieldId);
    if (!field) return;
    
    const isPassword = field.type === 'password';
    field.type = isPassword ? 'text' : 'password';
    
    const icon = toggleButton.querySelector('i');
    if (icon) {
        icon.className = isPassword ? 'fas fa-eye-slash' : 'fas fa-eye';
    }
    
    // Also toggle confirm password field if it exists
    const confirmField = document.getElementById('confirm_password');
    if (confirmField && fieldId === 'password') {
        confirmField.type = field.type;
    }
};

/**
 * ========================================
 * FORM VALIDATION
 * ========================================
 */
AuthModule.initializeFormValidation = function() {
    // Add real-time validation to all forms
    document.querySelectorAll('form').forEach(form => {
        const inputs = form.querySelectorAll('input, select, textarea');
        inputs.forEach(input => {
            input.addEventListener('blur', () => this.validateField(input));
            input.addEventListener('input', () => this.clearFieldError(input));
        });
    });
};

AuthModule.validateField = function(field) {
    const value = field.value.trim();
    const fieldType = field.type;
    const fieldName = field.name;
    
    // Clear previous errors
    this.clearFieldError(field);
    
    // Required field validation
    if (field.hasAttribute('required') && !value) {
        this.showFieldError(field, 'This field is required');
        return false;
    }
    
    // Email validation
    if (fieldType === 'email' && value && !this.config.emailRegex.test(value)) {
        this.showFieldError(field, 'Please enter a valid email address');
        return false;
    }
    
    // Password validation
    if (fieldName === 'password' && value) {
        const strength = this.calculatePasswordStrength(value);
        if (strength.score < 40) {
            this.showFieldError(field, 'Password is too weak');
            return false;
        }
    }
    
    // Password confirmation validation
    if (fieldName === 'confirm_password' && value) {
        const passwordField = document.getElementById('password');
        if (passwordField && passwordField.value !== value) {
            this.showFieldError(field, 'Passwords do not match');
            return false;
        }
    }
    
    return true;
};

AuthModule.showFieldError = function(field, message) {
    field.classList.add('is-invalid');
    
    const errorElement = document.getElementById(field.name + '-error') || 
                        document.getElementById(field.id + '-error');
    
    if (errorElement) {
        errorElement.textContent = message;
        errorElement.style.display = 'block';
    }
};

AuthModule.clearFieldError = function(field) {
    field.classList.remove('is-invalid');
    
    const errorElement = document.getElementById(field.name + '-error') || 
                        document.getElementById(field.id + '-error');
    
    if (errorElement) {
        errorElement.textContent = '';
        errorElement.style.display = 'none';
    }
};

/**
 * ========================================
 * PASSWORD STRENGTH CHECKER
 * ========================================
 */
AuthModule.checkPasswordStrength = function(password) {
    const strength = this.calculatePasswordStrength(password);
    const strengthBar = document.getElementById('passwordStrengthBar');
    const strengthText = document.getElementById('passwordStrengthText');
    
    if (!strengthBar || !strengthText) return;
    
    // Update progress bar
    strengthBar.style.width = strength.score + '%';
    strengthBar.className = `progress-bar bg-${strength.color}`;
    
    // Update text
    strengthText.textContent = `Password strength: ${strength.label}`;
    strengthText.className = `form-text text-${strength.color}`;
    
    // Show requirements
    this.updatePasswordRequirements(password);
    
    return strength;
};

AuthModule.calculatePasswordStrength = function(password) {
    let score = 0;
    let label = 'Very Weak';
    let color = 'danger';
    
    if (password.length >= 8) score += 20;
    if (password.length >= 12) score += 10;
    if (this.config.passwordRegex.lowercase.test(password)) score += 15;
    if (this.config.passwordRegex.uppercase.test(password)) score += 15;
    if (this.config.passwordRegex.number.test(password)) score += 15;
    if (this.config.passwordRegex.special.test(password)) score += 15;
    if (password.length >= 16) score += 10;
    
    if (score >= 80) {
        label = 'Very Strong';
        color = 'success';
    } else if (score >= 60) {
        label = 'Strong';
        color = 'info';
    } else if (score >= 40) {
        label = 'Good';
        color = 'warning';
    } else if (score >= 20) {
        label = 'Weak';
        color = 'warning';
    }
    
    return { score, label, color };
};

AuthModule.updatePasswordRequirements = function(password) {
    const requirements = [
        { id: 'req-length', met: password.length >= 8 },
        { id: 'req-lowercase', met: this.config.passwordRegex.lowercase.test(password) },
        { id: 'req-uppercase', met: this.config.passwordRegex.uppercase.test(password) },
        { id: 'req-number', met: this.config.passwordRegex.number.test(password) },
        { id: 'req-special', met: this.config.passwordRegex.special.test(password) }
    ];
    
    requirements.forEach(req => {
        const element = document.getElementById(req.id);
        if (element) {
            element.classList.toggle('text-success', req.met);
            element.classList.toggle('text-danger', !req.met);
            element.classList.remove('text-muted');
            const icon = element.querySelector('i');
            if (icon) {
                icon.className = req.met ? 'fas fa-check me-1' : 'fas fa-times me-1';
            }
        }
    });
};

AuthModule.validatePasswordMatch = function() {
    const passwordField = document.getElementById('password');
    const confirmPasswordField = document.getElementById('confirm_password');
    
    if (!passwordField || !confirmPasswordField) return true;
    
    const password = passwordField.value;
    const confirmPassword = confirmPasswordField.value;
    
    if (confirmPassword && password !== confirmPassword) {
        this.showFieldError(confirmPasswordField, 'Passwords do not match');
        return false;
    } else {
        this.clearFieldError(confirmPasswordField);
        return true;
    }
};

/**
 * ========================================
 * EMAIL VALIDATION
 * ========================================
 */
AuthModule.validateEmail = function(emailField) {
    const email = emailField.value.trim();
    
    if (!email) return true;
    
    if (!this.config.emailRegex.test(email)) {
        this.showFieldError(emailField, 'Please enter a valid email address');
        return false;
    }
    
    this.clearFieldError(emailField);
    return true;
};

AuthModule.checkEmailAvailability = function(email) {
    if (!email || !this.config.emailRegex.test(email)) return;
    
    // Don't check on login form
    if (document.getElementById('loginForm')) return;
    
    const checkEmailUrl = document.querySelector('[data-check-email-url]')?.dataset.checkEmailUrl;
    if (!checkEmailUrl) return;
    
    const csrfToken = this.getCsrfToken();

    fetch(checkEmailUrl, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-Requested-With': 'XMLHttpRequest',
            ...(csrfToken ? { 'X-CSRFToken': csrfToken } : {})
        },
        body: JSON.stringify({ email: email })
    })
    .then(response => response.json())
    .then(data => {
        const emailField = document.getElementById('email');
        if (!data.available) {
            this.showFieldError(emailField, 'This email is already registered');
        } else {
            this.clearFieldError(emailField);
        }
    })
    .catch(error => {
        console.error('Email availability check failed:', error);
    });
};

/**
 * ========================================
 * FORM SUBMISSION HANDLERS
 * ========================================
 */
/**
 * ========================================
 * FORM SUBMISSION
 * ========================================
 */
AuthModule.submitForm = async function(url, formData) {
    try {
        const csrfToken = this.getCsrfToken();
        const response = await fetch(url, {
            method: 'POST',
            body: formData,
            credentials: 'same-origin',
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                ...(csrfToken ? { 'X-CSRFToken': csrfToken } : {})
            }
        });
        
        const data = await response.json();
        
        // Check if response is successful
        if (!response.ok) {
            throw new Error(data.message || 'Request failed');
        }
        
        return data;
    } catch (error) {
        console.error('Form submission error:', error);
        throw error;
    }
};

AuthModule.handleLogin = function(e) {
    e.preventDefault();
    
    if (this.state.isSubmitting) return;
    
    const form = e.target;
    const formData = new FormData(form);
    
    // Validate form
    if (!this.validateForm(form)) return;
    
    // Set loading state
    this.setSubmissionState(true, 'Signing In...');
    
    // Submit login - use form action or default to /login
    const submitUrl = form.action || '/login';
    
    this.submitForm(submitUrl, formData)
        .then(data => {
            if (data.success) {
                this.showAlert('success', data.message || 'Login successful! Redirecting...');
                
                // Redirect after delay
                setTimeout(() => {
                    window.location.href = data.redirect_url || '/dashboard';
                }, 1000);
            } else {
                throw new Error(data.message || 'Login failed');
            }
        })
        .catch(error => {
            this.showAlert('error', error.message || 'Login failed. Please try again.');
        })
        .finally(() => {
            this.setSubmissionState(false);
        });
};

AuthModule.handleRegistration = function(e) {
    e.preventDefault();
    
    if (this.state.isSubmitting) return;
    
    const form = e.target;
    const formData = new FormData(form);
    
    // Validate form
    if (!this.validateForm(form)) return;
    
    // Additional validation
    if (!this.validatePasswordMatch()) return;
    
    // Check terms acceptance if checkbox exists
    const termsCheckbox = form.querySelector('#terms_accepted');
    if (termsCheckbox && !termsCheckbox.checked) {
        this.showFieldError(termsCheckbox, 'You must accept the terms to continue');
        return;
    }
    
    // Set loading state
    this.setSubmissionState(true, 'Creating account...');
    
    // Submit registration - use form action or default to /register
    const submitUrl = form.action || '/register';
    
    this.submitForm(submitUrl, formData)
        .then(data => {
            if (data.success) {
                this.showAlert('success', data.message || 'Account created successfully! Redirecting...');
                
                // Redirect after delay
                setTimeout(() => {
                    window.location.href = data.redirect_url || '/dashboard';
                }, 1000);
            } else {
                // Handle validation errors
                if (data.errors && Array.isArray(data.errors)) {
                    data.errors.forEach(error => {
                        this.showAlert('error', error);
                    });
                } else {
                    throw new Error(data.message || 'Registration failed');
                }
            }
        })
        .catch(error => {
            this.showAlert('error', error.message || 'Registration failed. Please try again.');
        })
        .finally(() => {
            this.setSubmissionState(false);
        });
};

AuthModule.handleForgotPassword = function(e) {
    e.preventDefault();
    
    if (this.state.isSubmitting) return;
    
    const form = e.target;
    const formData = new FormData(form);
    
    // Validate email
    const emailField = form.querySelector('#email');
    if (!this.validateEmail(emailField)) return;
    
    // Set loading state
    this.setSubmissionState(true, 'Sending reset email...');
    
    // Submit request
    this.submitForm(form.action, formData)
        .then(data => {
            if (data.success) {
                // Show success state
                this.showPasswordResetSuccess(emailField.value);
            } else {
                this.handleFormErrors(data);
            }
        })
        .finally(() => {
            this.setSubmissionState(false);
        });
};

/**
 * ========================================
 * FORM UTILITIES
 * ========================================
 */
AuthModule.validateForm = function(form) {
    const inputs = form.querySelectorAll('input[required], select[required], textarea[required]');
    let isValid = true;
    
    inputs.forEach(input => {
        if (!this.validateField(input)) {
            isValid = false;
        }
    });
    
    return isValid;
};

AuthModule.handleFormErrors = function(data) {
    if (data.errors) {
        Object.keys(data.errors).forEach(field => {
            const input = document.getElementById(field) || document.querySelector(`[name="${field}"]`);
            if (input) {
                const errorMessage = Array.isArray(data.errors[field]) ? 
                    data.errors[field][0] : data.errors[field];
                this.showFieldError(input, errorMessage);
            }
        });
    } else {
        this.showAlert('error', data.message || 'An error occurred. Please try again.');
    }
};

AuthModule.setSubmissionState = function(isSubmitting, loadingText = 'Loading...') {
    this.state.isSubmitting = isSubmitting;
    
    const submitButton = document.querySelector('button[type="submit"]');
    if (!submitButton) return;
    
    const btnText = submitButton.querySelector('.btn-text');
    const btnLoading = submitButton.querySelector('.btn-loading');
    
    if (isSubmitting) {
        if (btnText) btnText.classList.add('d-none');
        if (btnLoading) {
            btnLoading.classList.remove('d-none');
            const loadingTextElement = btnLoading.querySelector('.loading-text');
            if (loadingTextElement) {
                loadingTextElement.textContent = loadingText;
            }
        }
        submitButton.disabled = true;
    } else {
        if (btnText) btnText.classList.remove('d-none');
        if (btnLoading) btnLoading.classList.add('d-none');
        submitButton.disabled = false;
    }
};

/**
 * ========================================
 * SOCIAL LOGIN
 * ========================================
 */
AuthModule.handleSocialLogin = function(e) {
    e.preventDefault();
    
    const provider = e.target.dataset.socialLogin || 
                    e.target.closest('[data-social-login]')?.dataset.socialLogin;
    
    if (!provider) return;
    
    // Open social login popup
    const popupUrl = `/auth/social/${provider}`;
    const popup = window.open(
        popupUrl,
        'socialLogin',
        'width=600,height=600,scrollbars=yes,resizable=yes'
    );
    
    // Listen for popup completion
    const checkClosed = setInterval(() => {
        if (popup.closed) {
            clearInterval(checkClosed);
            // Reload page to check authentication status
            window.location.reload();
        }
    }, 1000);
};

/**
 * ========================================
 * UI HELPERS
 * ========================================
 */
AuthModule.showAlert = function(type, message) {
    // Use global alert system if available, otherwise create inline alert
    if (window.CognitiveCareerAI && window.CognitiveCareerAI.showAlert) {
        window.CognitiveCareerAI.showAlert(type, message);
        return;
    }

    const alertContainer = document.querySelector('.alert-container') || 
                          document.querySelector('.auth-card-body') ||
                          document.body;

    // Remove existing alerts to prevent duplicates
    const existingAlerts = alertContainer.querySelectorAll('.alert');
    existingAlerts.forEach(alert => alert.remove());

    const alertId = 'alert-' + Date.now();
    // Use a softer red for error alerts
    const customStyle = type === 'error' ? 'background-color: #ffeaea; color: #a94442; border-color: #f5c6cb;' : '';
    const alertHTML = `
        <div id="${alertId}" class="alert alert-${type === 'error' ? 'danger' : type} alert-dismissible fade show" role="alert" style="transition: opacity 0.5s; ${customStyle}">
            <i class="fas fa-${type === 'error' ? 'exclamation-circle' : 'check-circle'} me-2"></i>
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    `;

    alertContainer.insertAdjacentHTML('afterbegin', alertHTML);

    // Fade out after 8 seconds, but allow manual close
    setTimeout(() => {
        const alertElem = document.getElementById(alertId);
        if (alertElem) {
            alertElem.classList.remove('show');
            alertElem.classList.add('fade');
            setTimeout(() => { if (alertElem) alertElem.remove(); }, 500);
        }
    }, 8000);
};

AuthModule.showPasswordResetSuccess = function(email) {
    const form = document.getElementById('forgotPasswordForm');
    const successState = document.getElementById('successState');
    
    if (form && successState) {
        form.classList.add('d-none');
        successState.classList.remove('d-none');
        
        const emailSpan = document.getElementById('sentEmail');
        if (emailSpan) {
            emailSpan.textContent = email;
        }
    }
};

/**
 * ========================================
 * INITIALIZE MODULE
 * ========================================
 */
document.addEventListener('DOMContentLoaded', function() {
    AuthModule.init();
});

// Export for use in other modules
window.AuthModule = AuthModule;