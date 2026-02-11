/**
 * ========================================
 * DASHBOARD JAVASCRIPT MODULE
 * ========================================
 * Interactive dashboard functionality with animations and AI features
 */

'use strict';

// Dashboard module
const DashboardModule = {
    // Configuration
    config: {
        animationDuration: 300,
        counterAnimationDuration: 2000,
        fileUploadMaxSize: 5 * 1024 * 1024, // 5MB
        allowedFileTypes: ['pdf', 'doc', 'docx'],
        apiEndpoints: {
            uploadResume: '/api/resume/upload',
            getRecommendations: '/api/recommendations',
            getSkillsAssessment: '/api/skills/assessment'
        }
    },
    
    // State
    state: {
        isUploading: false,
        hasRecommendations: false,
        currentUser: null
    },
    
    // Initialize dashboard
    init: function() {
        this.setupEventListeners();
        this.initializeFileUpload();
        this.setupScrollAnimations();
        this.initializeCounters();
        this.loadUserData();
        
        console.log('🎯 Dashboard module initialized');
    }
};

/**
 * ========================================
 * EVENT LISTENERS SETUP
 * ========================================
 */
DashboardModule.setupEventListeners = function() {
    // Navigation events
    this.setupNavigationEvents();
    
    // File upload events
    this.setupFileUploadEvents();
    
    // Quick action events
    this.setupQuickActionEvents();
    
    // Profile completion events
    this.setupProfileEvents();
    
    // Assessment events
    this.setupAssessmentEvents();
    
    // Help and tutorial events
    this.setupHelpEvents();
};

DashboardModule.setupNavigationEvents = function() {
    // Upload Resume navigation
    document.getElementById('uploadResumeNav')?.addEventListener('click', (e) => {
        e.preventDefault();
        this.scrollToSection('fileDropZone');
    });
    
    // Careers navigation
    document.getElementById('careersNav')?.addEventListener('click', (e) => {
        e.preventDefault();
        this.explorecareers();
    });
    
    // Skills navigation
    document.getElementById('skillsNav')?.addEventListener('click', (e) => {
        e.preventDefault();
        this.startSkillsAssessment();
    });
    
    // Settings navigation
    document.getElementById('settingsLink')?.addEventListener('click', (e) => {
        e.preventDefault();
        this.openSettings();
    });
};

DashboardModule.setupFileUploadEvents = function() {
    const dropZone = document.getElementById('fileDropZone');
    const fileInput = document.getElementById('resumeUpload');
    
    if (!dropZone || !fileInput) return;
    
    // Click to upload
    dropZone.addEventListener('click', () => {
        if (!this.state.isUploading) {
            fileInput.click();
        }
    });
    
    // File input change
    fileInput.addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (file) {
            this.handleFileUpload(file);
        }
    });
    
    // Drag and drop events
    dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropZone.classList.add('dragover');
    });
    
    dropZone.addEventListener('dragleave', (e) => {
        e.preventDefault();
        dropZone.classList.remove('dragover');
    });
    
    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropZone.classList.remove('dragover');
        
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            this.handleFileUpload(files[0]);
        }
    });
};

DashboardModule.setupQuickActionEvents = function() {
    // Get Started button
    document.getElementById('getStartedBtn')?.addEventListener('click', () => {
        this.getPersonalizedRecommendations();
    });
    
    // Explore button
    document.getElementById('exploreBtn')?.addEventListener('click', () => {
        this.explorecareers();
    });
    
    // Start Assessment button
    document.getElementById('startAssessmentBtn')?.addEventListener('click', () => {
        this.startSkillsAssessment();
    });
    
    // Action buttons
    document.querySelectorAll('.action-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            const action = e.currentTarget.querySelector('span').textContent.trim().toLowerCase();
            this.handleQuickAction(action);
        });
    });
};

DashboardModule.setupProfileEvents = function() {
    // Profile completion tasks
    document.querySelectorAll('.task-item:not(.completed)').forEach(task => {
        task.addEventListener('click', () => {
            window.location.href = '/auth/profile';
        });
    });
};

DashboardModule.setupAssessmentEvents = function() {
    // Skills badges interaction
    document.querySelectorAll('.skill-badge').forEach(badge => {
        badge.addEventListener('click', () => {
            badge.classList.add('animate-pulse');
            setTimeout(() => {
                badge.classList.remove('animate-pulse');
            }, 600);
        });
    });
};

DashboardModule.setupHelpEvents = function() {
    // Floating help button
    document.querySelector('.floating-help button')?.addEventListener('click', () => {
        this.showHelpModal();
    });
};

/**
 * ========================================
 * FILE UPLOAD FUNCTIONALITY
 * ========================================
 */
DashboardModule.initializeFileUpload = function() {
    // Add drag and drop styles
    const style = document.createElement('style');
    style.textContent = `
        .file-drop-zone {
            border: 2px dashed #dee2e6;
            border-radius: 8px;
            padding: 2rem;
            text-align: center;
            transition: all 0.3s ease;
            cursor: pointer;
            background: #f8f9fa;
        }
        
        .file-drop-zone:hover {
            border-color: #007bff;
            background: #e3f2fd;
        }
        
        .file-drop-zone.dragover {
            border-color: #007bff;
            background: #e3f2fd;
            transform: scale(1.02);
        }
        
        .drop-icon {
            font-size: 3rem;
            color: #6c757d;
            margin-bottom: 1rem;
        }
        
        .file-drop-zone:hover .drop-icon {
            color: #007bff;
            animation: bounce 0.6s ease;
        }
    `;
    document.head.appendChild(style);
};

DashboardModule.handleFileUpload = function(file) {
    // Validate file
    const validation = this.validateFile(file);
    if (!validation.valid) {
        this.showAlert('error', validation.message);
        return;
    }
    
    // Start upload
    this.state.isUploading = true;
    this.showUploadProgress();
    
    // Create form data
    const formData = new FormData();
    formData.append('resume', file);
    
    // Upload file
    this.uploadResumeFile(formData)
        .then(response => {
            if (response.success) {
                this.handleUploadSuccess(response);
            } else {
                this.handleUploadError(response.message);
            }
        })
        .catch(error => {
            this.handleUploadError('Upload failed. Please try again.');
        })
        .finally(() => {
            this.state.isUploading = false;
            this.hideUploadProgress();
        });
};

DashboardModule.validateFile = function(file) {
    // Check file size
    if (file.size > this.config.fileUploadMaxSize) {
        return {
            valid: false,
            message: 'File size must be less than 5MB'
        };
    }
    
    // Check file type
    const extension = file.name.split('.').pop().toLowerCase();
    if (!this.config.allowedFileTypes.includes(extension)) {
        return {
            valid: false,
            message: 'Please upload a PDF, DOC, or DOCX file'
        };
    }
    
    return { valid: true };
};

DashboardModule.uploadResumeFile = async function(formData) {
    try {
        const response = await fetch(this.config.apiEndpoints.uploadResume, {
            method: 'POST',
            body: formData,
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error('Upload error:', error);
        throw error;
    }
};

DashboardModule.showUploadProgress = function() {
    const dropContent = document.querySelector('.drop-zone-content');
    const progressSection = document.querySelector('.upload-progress');
    
    if (dropContent) dropContent.classList.add('d-none');
    if (progressSection) {
        progressSection.classList.remove('d-none');
        this.animateProgressBar();
    }
};

DashboardModule.hideUploadProgress = function() {
    const dropContent = document.querySelector('.drop-zone-content');
    const progressSection = document.querySelector('.upload-progress');
    
    if (progressSection) progressSection.classList.add('d-none');
    if (dropContent) dropContent.classList.remove('d-none');
};

DashboardModule.animateProgressBar = function() {
    const progressBar = document.querySelector('.upload-progress .progress-bar');
    if (!progressBar) return;
    
    let progress = 0;
    const interval = setInterval(() => {
        progress += Math.random() * 20;
        if (progress > 90) {
            progress = 90;
        }
        
        progressBar.style.width = `${progress}%`;
        
        if (progress >= 90) {
            clearInterval(interval);
        }
    }, 200);
};

DashboardModule.handleUploadSuccess = function(response) {
    // Complete progress bar
    const progressBar = document.querySelector('.upload-progress .progress-bar');
    if (progressBar) {
        progressBar.style.width = '100%';
    }
    
    // Show success message
    this.showAlert('success', 'Resume uploaded successfully! Generating recommendations...');
    
    // Update stats
    this.updateStats(response.stats);
    
    // Load recommendations
    setTimeout(() => {
        this.loadRecommendations(response.analysis);
    }, 1000);
};

DashboardModule.handleUploadError = function(message) {
    this.showAlert('error', message);
    this.shakeElement('.file-drop-zone');
};

/**
 * ========================================
 * RECOMMENDATIONS SYSTEM
 * ========================================
 */
DashboardModule.getPersonalizedRecommendations = function() {
    this.showLoadingOverlay('Generating personalized recommendations...');
    
    fetch(this.config.apiEndpoints.getRecommendations)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                this.displayRecommendations(data.recommendations);
            } else {
                this.showAlert('warning', 'Please upload your resume first to get personalized recommendations.');
                this.scrollToSection('fileDropZone');
            }
        })
        .catch(error => {
            this.showAlert('error', 'Failed to load recommendations. Please try again.');
        })
        .finally(() => {
            this.hideLoadingOverlay();
        });
};

DashboardModule.loadRecommendations = function(analysis) {
    const recommendationsContainer = document.querySelector('.recommendations-placeholder');
    const recommendationsList = document.getElementById('recommendationsList');
    
    if (!recommendationsContainer || !recommendationsList) return;
    
    // Hide placeholder
    recommendationsContainer.classList.add('d-none');
    
    // Show recommendations
    recommendationsList.classList.remove('d-none');
    recommendationsList.innerHTML = this.generateRecommendationsHTML(analysis.recommendations);
    
    // Animate recommendations
    this.animateRecommendations();
    
    // Update state
    this.state.hasRecommendations = true;
};

DashboardModule.generateRecommendationsHTML = function(recommendations) {
    return recommendations.map((rec, index) => `
        <div class="recommendation-item mb-3 animate-fadeInUp" style="animation-delay: ${index * 0.1}s">
            <div class="d-flex align-items-center">
                <div class="rec-icon me-3">
                    <i class="fas fa-briefcase text-primary"></i>
                </div>
                <div class="flex-grow-1">
                    <h6 class="mb-1">${rec.title}</h6>
                    <small class="text-muted">${rec.match_percentage}% match</small>
                    <div class="progress mt-1" style="height: 4px;">
                        <div class="progress-bar" style="width: ${rec.match_percentage}%"></div>
                    </div>
                </div>
                <div class="rec-actions">
                    <button class="btn btn-sm btn-outline-primary" onclick="DashboardModule.exploreCareer('${rec.id}')">
                        <i class="fas fa-external-link-alt"></i>
                    </button>
                </div>
            </div>
        </div>
    `).join('');
};

DashboardModule.animateRecommendations = function() {
    const recommendations = document.querySelectorAll('.recommendation-item');
    recommendations.forEach((rec, index) => {
        setTimeout(() => {
            rec.classList.add('animate-slideInLeft');
        }, index * 100);
    });
};

/**
 * ========================================
 * QUICK ACTIONS
 * ========================================
 */
DashboardModule.handleQuickAction = function(action) {
    switch (action) {
        case 'job search':
            this.openJobSearch();
            break;
        case 'skill map':
            this.openSkillMap();
            break;
        case 'career path':
            this.openCareerPath();
            break;
        case 'learning':
            this.openLearning();
            break;
        default:
            console.log('Unknown action:', action);
    }
};

DashboardModule.exploreCareer = function(careerId) {
    this.showModal({
        title: 'Career Details',
        body: 'Loading career information...',
        size: 'lg'
    });
    
    // Load career details (placeholder)
    setTimeout(() => {
        this.updateModalContent({
            body: `
                <div class="career-details">
                    <h5>Software Developer</h5>
                    <p>Match: 95%</p>
                    <h6>Required Skills:</h6>
                    <div class="skills-list">
                        <span class="badge bg-primary me-2">JavaScript</span>
                        <span class="badge bg-primary me-2">Python</span>
                        <span class="badge bg-primary me-2">React</span>
                    </div>
                    <h6 class="mt-3">Job Opportunities:</h6>
                    <p>Currently 1,234 open positions in your area.</p>
                </div>
            `
        });
    }, 1000);
};

DashboardModule.explorecareers = function() {
    this.showAlert('info', 'Career exploration feature coming soon!');
};

DashboardModule.startSkillsAssessment = function() {
    this.showModal({
        title: 'Skills Assessment',
        body: `
            <div class="assessment-intro text-center">
                <i class="fas fa-graduation-cap fa-3x text-primary mb-3"></i>
                <h5>Ready to assess your skills?</h5>
                <p>This comprehensive assessment will help identify your strengths and growth areas.</p>
                <p><strong>Duration:</strong> 15-20 minutes</p>
                <button class="btn btn-primary btn-lg" onclick="DashboardModule.launchAssessment()">
                    <i class="fas fa-play me-2"></i>Start Assessment
                </button>
            </div>
        `,
        size: 'lg'
    });
};

DashboardModule.launchAssessment = function() {
    this.hideModal();
    this.showAlert('info', 'Skills assessment feature coming soon!');
};

/**
 * ========================================
 * UI UTILITIES
 * ========================================
 */
DashboardModule.initializeCounters = function() {
    const counters = document.querySelectorAll('.counter');
    
    const observerOptions = {
        threshold: 0.7
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                this.animateCounter(entry.target);
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);
    
    counters.forEach(counter => observer.observe(counter));
};

DashboardModule.animateCounter = function(element) {
    const target = parseInt(element.dataset.target) || 0;
    const duration = this.config.counterAnimationDuration;
    const step = target / (duration / 16);
    let current = 0;
    
    const timer = setInterval(() => {
        current += step;
        if (current >= target) {
            current = target;
            clearInterval(timer);
        }
        element.textContent = Math.floor(current).toLocaleString();
    }, 16);
};

DashboardModule.setupScrollAnimations = function() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-fadeInUp');
            }
        });
    }, observerOptions);
    
    // Observe all cards and sections
    document.querySelectorAll('.card, .feature-card').forEach(el => {
        observer.observe(el);
    });
};

DashboardModule.scrollToSection = function(sectionId) {
    const element = document.getElementById(sectionId);
    if (element) {
        element.scrollIntoView({
            behavior: 'smooth',
            block: 'center'
        });
        
        // Add highlight effect
        element.classList.add('animate-pulse');
        setTimeout(() => {
            element.classList.remove('animate-pulse');
        }, 2000);
    }
};

DashboardModule.shakeElement = function(selector) {
    const element = document.querySelector(selector);
    if (element) {
        element.classList.add('animate-shake');
        setTimeout(() => {
            element.classList.remove('animate-shake');
        }, 600);
    }
};

DashboardModule.showLoadingOverlay = function(message = 'Loading...') {
    const overlay = document.getElementById('loadingOverlay');
    if (overlay) {
        overlay.querySelector('p').textContent = message;
        overlay.classList.remove('d-none');
    }
};

DashboardModule.hideLoadingOverlay = function() {
    const overlay = document.getElementById('loadingOverlay');
    if (overlay) {
        overlay.classList.add('d-none');
    }
};

DashboardModule.showAlert = function(type, message) {
    // Use global alert system if available
    if (window.CognitiveCareerAI && window.CognitiveCareerAI.showAlert) {
        window.CognitiveCareerAI.showAlert(type, message);
        return;
    }
    
    // Create alert element
    const alertHTML = `
        <div class="alert alert-${type === 'error' ? 'danger' : type} alert-dismissible fade show notification-slide-in" role="alert" style="position: fixed; top: 20px; right: 20px; z-index: 9999; min-width: 300px;">
            <i class="fas fa-${this.getAlertIcon(type)} me-2"></i>
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    `;
    
    document.body.insertAdjacentHTML('beforeend', alertHTML);
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        const alert = document.querySelector('.alert:last-of-type');
        if (alert) {
            alert.classList.add('notification-slide-out');
            setTimeout(() => alert.remove(), 400);
        }
    }, 5000);
};

DashboardModule.getAlertIcon = function(type) {
    const icons = {
        success: 'check-circle',
        error: 'exclamation-circle',
        warning: 'exclamation-triangle',
        info: 'info-circle'
    };
    return icons[type] || 'info-circle';
};

DashboardModule.showModal = function(options) {
    const modalHTML = `
        <div class="modal fade" id="dynamicModal" tabindex="-1">
            <div class="modal-dialog ${options.size ? 'modal-' + options.size : ''}">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">${options.title}</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        ${options.body}
                    </div>
                    ${options.footer ? `<div class="modal-footer">${options.footer}</div>` : ''}
                </div>
            </div>
        </div>
    `;
    
    // Remove existing modal
    const existingModal = document.getElementById('dynamicModal');
    if (existingModal) {
        existingModal.remove();
    }
    
    // Add new modal
    document.body.insertAdjacentHTML('beforeend', modalHTML);
    
    // Show modal
    const modal = new bootstrap.Modal(document.getElementById('dynamicModal'));
    modal.show();
    
    return modal;
};

DashboardModule.updateModalContent = function(options) {
    const modal = document.getElementById('dynamicModal');
    if (modal) {
        if (options.title) {
            modal.querySelector('.modal-title').textContent = options.title;
        }
        if (options.body) {
            modal.querySelector('.modal-body').innerHTML = options.body;
        }
        if (options.footer) {
            modal.querySelector('.modal-footer').innerHTML = options.footer;
        }
    }
};

DashboardModule.hideModal = function() {
    const modal = document.getElementById('dynamicModal');
    if (modal) {
        bootstrap.Modal.getInstance(modal).hide();
    }
};

/**
 * ========================================
 * DATA MANAGEMENT
 * ========================================
 */
DashboardModule.loadUserData = function() {
    // Load user data from server or local storage
    this.state.currentUser = {
        name: 'User',
        profileCompletion: 75,
        resumesCount: 0,
        matchesCount: 0,
        skillsCount: 0
    };
};

DashboardModule.updateStats = function(stats) {
    if (stats.resumesAnalyzed !== undefined) {
        this.updateCounter('[data-target]', stats.resumesAnalyzed);
    }
    if (stats.careerMatches !== undefined) {
        this.updateCounter('[data-target]', stats.careerMatches);
    }
    if (stats.skillsIdentified !== undefined) {
        this.updateCounter('[data-target]', stats.skillsIdentified);
    }
};

DashboardModule.updateCounter = function(selector, newValue) {
    const counter = document.querySelector(selector);
    if (counter) {
        counter.dataset.target = newValue;
        this.animateCounter(counter);
    }
};

// Global functions for template usage
window.animateCounters = function() {
    DashboardModule.initializeCounters();
};

window.DashboardModule = DashboardModule;