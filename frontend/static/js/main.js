/**
 * ========================================
 * COGNITIVE CAREER AI - MAIN JAVASCRIPT
 * ========================================
 * Core functionality and utilities
 */

'use strict';

// Global app configuration
const CognitiveCareerAI = {
    // API endpoints
    api: {
        base: '/api/v1',
        auth: '/auth',
        ai: '/ai',
        user: '/user'
    },
    
    // Application state
    state: {
        isLoading: false,
        currentUser: null,
        theme: 'light'
    },
    
    // Utility functions
    utils: {},
    
    // Component modules
    components: {},
    
    // Initialize the app
    init: function() {
        this.initializeTheme();
        this.setupGlobalEventListeners();
        this.initializeTooltips();
        this.initializeModals();
        this.loadUserState();
    }
};

/**
 * ========================================
 * THEME MANAGEMENT
 * ========================================
 */
CognitiveCareerAI.initializeTheme = function() {
    const savedTheme = localStorage.getItem('theme') || 'light';
    const htmlElement = document.documentElement;
    const themeToggle = document.getElementById('theme-toggle');
    
    // Set initial theme
    htmlElement.setAttribute('data-bs-theme', savedTheme);
    this.state.theme = savedTheme;
    
    // Update theme toggle icon
    this.updateThemeIcon();
    
    // Theme toggle listener
    if (themeToggle) {
        themeToggle.addEventListener('click', () => {
            this.toggleTheme();
        });
    }
};

CognitiveCareerAI.toggleTheme = function() {
    const htmlElement = document.documentElement;
    const currentTheme = htmlElement.getAttribute('data-bs-theme');
    const newTheme = currentTheme === 'light' ? 'dark' : 'light';
    
    htmlElement.setAttribute('data-bs-theme', newTheme);
    localStorage.setItem('theme', newTheme);
    this.state.theme = newTheme;
    
    this.updateThemeIcon();
    
    // Dispatch theme change event
    document.dispatchEvent(new CustomEvent('themeChanged', { 
        detail: { theme: newTheme }
    }));
};

CognitiveCareerAI.updateThemeIcon = function() {
    const themeToggle = document.getElementById('theme-toggle');
    if (!themeToggle) return;
    
    const icon = themeToggle.querySelector('i');
    const isDark = this.state.theme === 'dark';
    
    if (icon) {
        // Update icon class
        icon.className = isDark ? 'fas fa-sun' : 'fas fa-moon';
        // Inline styles to ensure visibility
        icon.style.color = isDark ? '#ffa500' : '#333';
        icon.style.fontSize = '18px';
        icon.style.lineHeight = '1';
        icon.style.display = 'inline-block';
    }
    
    // Update button styling
    themeToggle.style.backgroundColor = isDark ? '#454d55' : '#f8f9fa';
    themeToggle.style.borderColor = isDark ? '#6c757d' : '#dee2e6';
};

/**
 * ========================================
 * GLOBAL EVENT LISTENERS
 * ========================================
 */
CognitiveCareerAI.setupGlobalEventListeners = function() {
    // Global click handler
    document.addEventListener('click', (e) => {
        // Handle any global click events
        this.handleGlobalClick(e);
    });
    
    // Form submission handler
    document.addEventListener('submit', (e) => {
        // Add loading indicators to form submissions
        this.handleFormSubmission(e);
    });
    
    // Window resize handler
    window.addEventListener('resize', this.utils.debounce(() => {
        this.handleWindowResize();
    }, 250));
    
    // Online/offline handlers
    window.addEventListener('online', () => {
        this.showAlert('success', 'Connection restored!');
        this.state.isOnline = true;
    });
    
    window.addEventListener('offline', () => {
        this.showAlert('warning', 'You are currently offline. Some features may not work.');
        this.state.isOnline = false;
    });
};

CognitiveCareerAI.handleGlobalClick = function(e) {
    // Handle dropdown auto-close
    if (e.target.closest('.dropdown-menu')) return;
    
    // Close any open dropdowns that aren't Bootstrap managed
    const customDropdowns = document.querySelectorAll('.custom-dropdown.show');
    customDropdowns.forEach(dropdown => {
        dropdown.classList.remove('show');
    });
};

CognitiveCareerAI.handleFormSubmission = function(e) {
    // Add automatic loading states to buttons
    const form = e.target;
    const submitButton = form.querySelector('button[type="submit"]');
    
    if (submitButton && !submitButton.hasAttribute('data-no-loading')) {
        const originalHTML = submitButton.innerHTML;
        
        // Set loading state
        submitButton.innerHTML = `
            <span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
            Loading...
        `;
        submitButton.disabled = true;
        
        // Reset after 5 seconds if form hasn't been handled
        setTimeout(() => {
            if (submitButton.disabled) {
                submitButton.innerHTML = originalHTML;
                submitButton.disabled = false;
            }
        }, 5000);
    }
};

CognitiveCareerAI.handleWindowResize = function() {
    // Handle responsive behavior
    this.updateResponsiveElements();
};

/**
 * ========================================
 * BOOTSTRAP COMPONENT INITIALIZATION
 * ========================================
 */
CognitiveCareerAI.initializeTooltips = function() {
    // Initialize Bootstrap tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
};

CognitiveCareerAI.initializeModals = function() {
    // Initialize any custom modal behaviors
    const modals = document.querySelectorAll('.modal');
    modals.forEach(modal => {
        modal.addEventListener('shown.bs.modal', function () {
            const firstInput = this.querySelector('input:not([type="hidden"]), textarea, select');
            if (firstInput) {
                firstInput.focus();
            }
        });
    });
};

/**
 * ========================================
 * UTILITY FUNCTIONS
 * ========================================
 */
CognitiveCareerAI.utils.debounce = function(func, wait, immediate) {
    let timeout;
    return function executedFunction() {
        const context = this;
        const args = arguments;
        const later = function() {
            timeout = null;
            if (!immediate) func.apply(context, args);
        };
        const callNow = immediate && !timeout;
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
        if (callNow) func.apply(context, args);
    };
};

CognitiveCareerAI.utils.throttle = function(func, limit) {
    let inThrottle;
    return function() {
        const args = arguments;
        const context = this;
        if (!inThrottle) {
            func.apply(context, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    }
};

CognitiveCareerAI.utils.formatCurrency = function(amount, currency = 'USD') {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: currency,
        minimumFractionDigits: 0,
        maximumFractionDigits: 0
    }).format(amount);
};

CognitiveCareerAI.utils.formatDate = function(date, options = {}) {
    const defaultOptions = {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    };
    const formatOptions = { ...defaultOptions, ...options };
    return new Intl.DateTimeFormat('en-US', formatOptions).format(new Date(date));
};

CognitiveCareerAI.utils.escapeHtml = function(text) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, function(m) { return map[m]; });
};

/**
 * ========================================
 * API HELPERS
 * ========================================
 */
CognitiveCareerAI.api.request = async function(url, options = {}) {
    const defaultOptions = {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'X-Requested-With': 'XMLHttpRequest'
        },
        credentials: 'same-origin'
    };
    
    const requestOptions = { ...defaultOptions, ...options };
    
    // Add CSRF token if available
    const csrfToken = document.querySelector('meta[name="csrf-token"]')?.content;
    if (csrfToken && !requestOptions.headers['X-CSRFToken']) {
        requestOptions.headers['X-CSRFToken'] = csrfToken;
    }
    
    try {
        CognitiveCareerAI.state.isLoading = true;
        
        const response = await fetch(url, requestOptions);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        return data;
        
    } catch (error) {
        console.error('API request failed:', error);
        CognitiveCareerAI.showAlert('error', 'Network error. Please try again.');
        throw error;
    } finally {
        CognitiveCareerAI.state.isLoading = false;
    }
};

CognitiveCareerAI.api.get = function(url, options = {}) {
    return this.request(url, { ...options, method: 'GET' });
};

CognitiveCareerAI.api.post = function(url, data, options = {}) {
    return this.request(url, {
        ...options,
        method: 'POST',
        body: JSON.stringify(data)
    });
};

CognitiveCareerAI.api.put = function(url, data, options = {}) {
    return this.request(url, {
        ...options,
        method: 'PUT',
        body: JSON.stringify(data)
    });
};

CognitiveCareerAI.api.delete = function(url, options = {}) {
    return this.request(url, { ...options, method: 'DELETE' });
};

/**
 * ========================================
 * ALERT SYSTEM
 * ========================================
 */
CognitiveCareerAI.showAlert = function(type, message, options = {}) {
    const alertContainer = this.getAlertContainer();
    const alertId = 'alert-' + Date.now();
    
    // Remove previous error alerts to prevent duplicates
    const existingAlerts = alertContainer.querySelectorAll('.alert');
    existingAlerts.forEach(alert => {
        const alertType = alert.classList.contains('alert-danger') ? 'error' : 
                         alert.classList.contains('alert-success') ? 'success' :
                         alert.classList.contains('alert-warning') ? 'warning' : 'info';
        
        // Remove if same type or if too many alerts (max 3)
        if (alertType === type || existingAlerts.length >= 3) {
            alert.remove();
        }
    });
    
    const alertHTML = `
        <div class="alert alert-${type === 'error' ? 'danger' : type} alert-dismissible fade show" role="alert" id="${alertId}">
            <i class="fas fa-${this.getAlertIcon(type)} me-2"></i>
            <strong>${this.getAlertTitle(type)}</strong> ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>
    `;
    
    alertContainer.insertAdjacentHTML('beforeend', alertHTML);
    
    // Auto-dismiss alerts based on type (unless persistent is set)
    if (options.persistent !== true) {
        let duration = 15000; // Default: 15 seconds
        
        // Set duration based on alert type
        switch(type) {
            case 'warning':
                duration = options.duration || 2500; // Warning: 2.5 seconds
                break;
            case 'error':
                duration = options.duration || 5000; // Error: 5 seconds
                break;
            case 'success':
            case 'info':
                duration = options.duration || 15000; // Success/info: 15 seconds
                break;
            default:
                duration = options.duration || 3000; // Others: 3 seconds
        }
        
        // Auto-dismiss the alert
        setTimeout(() => {
            const alertElement = document.getElementById(alertId);
            if (alertElement) {
                // Trigger Bootstrap's fade-out animation then remove
                alertElement.classList.remove('show');
                setTimeout(() => {
                    if (alertElement.parentElement) {
                        alertElement.remove();
                    }
                }, 150); // Give time for fade animation
            }
        }, duration);
    }
};

CognitiveCareerAI.getAlertContainer = function() {
    let container = document.getElementById('global-alerts');
    
    if (!container) {
        container = document.createElement('div');
        container.id = 'global-alerts';
        container.className = 'position-fixed top-0 end-0 p-3';
        container.style.zIndex = '1060';
        document.body.appendChild(container);
    }
    
    return container;
};

CognitiveCareerAI.getAlertIcon = function(type) {
    const icons = {
        success: 'check-circle',
        error: 'exclamation-circle',
        warning: 'exclamation-triangle',
        info: 'info-circle'
    };
    return icons[type] || 'info-circle';
};

CognitiveCareerAI.getAlertTitle = function(type) {
    const titles = {
        success: 'Success!',
        error: 'Error!',
        warning: 'Warning!',
        info: 'Info:'
    };
    return titles[type] || 'Notice:';
};

/**
 * ========================================
 * USER STATE MANAGEMENT
 * ========================================
 */
CognitiveCareerAI.loadUserState = function() {
    // Load user data from meta tag or API
    const userDataElement = document.querySelector('meta[name="user-data"]');
    if (userDataElement) {
        try {
            const userData = JSON.parse(userDataElement.content);
            this.state.currentUser = userData;
        } catch (error) {
            console.warn('Failed to parse user data:', error);
        }
    }
};

/**
 * ========================================
 * RESPONSIVE UTILITIES
 * ========================================
 */
CognitiveCareerAI.updateResponsiveElements = function() {
    // Update any elements that need responsive behavior
    const isMobile = window.innerWidth < 768;
    const isTablet = window.innerWidth >= 768 && window.innerWidth < 1200;
    
    document.body.classList.toggle('is-mobile', isMobile);
    document.body.classList.toggle('is-tablet', isTablet);
    document.body.classList.toggle('is-desktop', !isMobile && !isTablet);
};

/**
 * ========================================
 * PERFORMANCE MONITORING
 * ========================================
 */
CognitiveCareerAI.trackPageLoad = function() {
    // Track page load performance
    if ('performance' in window) {
        window.addEventListener('load', () => {
            const loadTime = performance.now();
            // Performance tracking (silent in production)
        });
    }
};

/**
 * ========================================
 * ACCESSIBILITY HELPERS
 * ========================================
 */
CognitiveCareerAI.announceToScreenReader = function(message) {
    const announcement = document.createElement('div');
    announcement.setAttribute('role', 'status');
    announcement.setAttribute('aria-live', 'polite');
    announcement.className = 'sr-only';
    announcement.textContent = message;
    
    document.body.appendChild(announcement);
    
    setTimeout(() => {
        document.body.removeChild(announcement);
    }, 1000);
};

CognitiveCareerAI.trapFocus = function(element) {
    const focusableElements = element.querySelectorAll(
        'a[href], button:not([disabled]), textarea:not([disabled]), input[type="text"]:not([disabled]), input[type="radio"]:not([disabled]), input[type="checkbox"]:not([disabled]), select:not([disabled])'
    );
    
    const firstFocusable = focusableElements[0];
    const lastFocusable = focusableElements[focusableElements.length - 1];
    
    element.addEventListener('keydown', (e) => {
        if (e.key === 'Tab') {
            if (e.shiftKey && document.activeElement === firstFocusable) {
                e.preventDefault();
                lastFocusable.focus();
            } else if (!e.shiftKey && document.activeElement === lastFocusable) {
                e.preventDefault();
                firstFocusable.focus();
            }
        }
    });
};

/**
 * ========================================
 * INITIALIZE ON DOM READY
 * ========================================
 */
document.addEventListener('DOMContentLoaded', function() {
    CognitiveCareerAI.init();
});

// Export for use in other modules
window.CognitiveCareerAI = CognitiveCareerAI;