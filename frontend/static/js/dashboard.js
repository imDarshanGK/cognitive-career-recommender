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
            uploadResume: '/upload_resume',
            analyzeProfile: '/analyze_profile',
            feedback: '/feedback',
            feedbackHistory: '/api/feedback'
        }
    },
    
    // State
    state: {
        isUploading: false,
        hasRecommendations: false,
        currentUser: null,
        lastProfile: null,
        lastSkills: []
    },
    
    // Initialize dashboard
    init: function() {
        this.setupEventListeners();
        this.initializeFileUpload();
        this.setupScrollAnimations();
        this.loadUserData();
        this.loadFeedbackHistory();
        
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

    // Manual profile events
    this.setupManualProfileEvents();
    
    // Primary action events
    this.setupQuickActionEvents();
};

DashboardModule.setupNavigationEvents = function() {
    // Upload Resume navigation
    document.getElementById('uploadResumeNav')?.addEventListener('click', (e) => {
        e.preventDefault();
        this.scrollToSection('fileDropZone');
    });

    // Manual profile navigation
    document.getElementById('manualProfileNav')?.addEventListener('click', (e) => {
        e.preventDefault();
        this.scrollToSection('manual-profile');
    });
    
    // Careers navigation
    document.getElementById('careersNav')?.addEventListener('click', (e) => {
        e.preventDefault();
        this.explorecareers();
    });
    
    // Skills navigation
    document.getElementById('skillsNav')?.addEventListener('click', (e) => {
        e.preventDefault();
        this.scrollToSection('skill-gap');
    });

    // Roadmap navigation
    document.getElementById('roadmapNav')?.addEventListener('click', (e) => {
        e.preventDefault();
        this.scrollToSection('roadmap');
    });

    // Feedback navigation
    document.getElementById('feedbackNav')?.addEventListener('click', (e) => {
        e.preventDefault();
        this.scrollToSection('feedback');
    });
    
    return;
};

DashboardModule.setupManualProfileEvents = function() {
    const form = document.getElementById('manualProfileForm');
    if (!form) return;

    form.addEventListener('submit', (e) => {
        e.preventDefault();
        this.handleManualProfileSubmit();
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
};

/**
 * ========================================
 * FILE UPLOAD FUNCTIONALITY
 * ========================================
 */
DashboardModule.initializeFileUpload = function() {
    // Styling handled by dashboard.css
    return;
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
            if (response && (response.error || response.status === 'error')) {
                this.handleUploadError(response.error || response.message || 'Upload failed.');
            } else {
                this.handleUploadSuccess(response);
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

    if (response && (response.error || response.status === 'error')) {
        this.showAlert('error', response.error || response.message || 'Resume analysis failed.');
        return;
    }
    
    // Show success message
    this.showAlert('success', 'Resume uploaded successfully. Building your profile...');

    // Build profile data from resume response
    const profilePayload = this.buildProfileFromResume(response);
    if (!profilePayload) {
        this.showAlert('warning', 'Resume parsed, but no usable profile data was found. Try manual profile input.');
        return;
    }

    this.setProfileStatus('Resume parsed');
    this.submitProfileForAnalysis(profilePayload, profilePayload.skills || []);
};

DashboardModule.handleUploadError = function(message) {
    this.showAlert('error', message);
    this.shakeElement('.file-drop-zone');
};

DashboardModule.handleManualProfileSubmit = function() {
    const educationLevel = document.getElementById('educationLevel')?.value.trim();
    const yearsExperienceRaw = document.getElementById('yearsExperience')?.value;
    const skillsInput = document.getElementById('skillsInput')?.value || '';
    const interestArea = document.getElementById('interestArea')?.value || '';

    const skills = this.normalizeSkills(skillsInput);
    const interests = this.normalizeSkills(interestArea);
    const yearsExperience = yearsExperienceRaw ? parseFloat(yearsExperienceRaw) : 0;

    if (!educationLevel && skills.length === 0 && interests.length === 0 && !yearsExperience) {
        this.showAlert('warning', 'Add at least one skill, education level, or interest to continue.');
        return;
    }

    const payload = {
        skills: skills,
        interests: interests,
        education: { degrees: educationLevel ? [educationLevel] : [] },
        experience: yearsExperience ? [{ years: yearsExperience }] : []
    };

    this.state.lastProfile = payload;
    this.state.lastSkills = skills;
    this.setProfileStatus('Manual profile ready');
    this.submitProfileForAnalysis(payload, skills);
};

DashboardModule.buildProfileFromResume = function(response) {
    if (!response) return null;

    if (response.structured_profile) {
        return response.structured_profile;
    }

    const skills = [];
    if (response.skills) {
        if (Array.isArray(response.skills)) {
            skills.push(...response.skills);
        } else {
            const technical = response.skills.technical_skills || [];
            const soft = response.skills.soft_skills || [];
            skills.push(...technical, ...soft);
        }
    }

    if (response.resume_data && response.resume_data.skills) {
        const resumeSkills = response.resume_data.skills;
        if (Array.isArray(resumeSkills)) {
            skills.push(...resumeSkills);
        } else {
            skills.push(...(resumeSkills.technical_skills || []), ...(resumeSkills.soft_skills || []));
        }
    }

    if (response.data && response.data.skills && Array.isArray(response.data.skills)) {
        skills.push(...response.data.skills);
    }

    const educationDegrees = [];
    if (response.education) {
        if (response.education.degree) {
            educationDegrees.push(response.education.degree);
        }
        if (Array.isArray(response.education.degrees)) {
            educationDegrees.push(...response.education.degrees);
        }
    }

    if (response.resume_data && response.resume_data.education) {
        const resumeEdu = response.resume_data.education;
        if (resumeEdu.degree) {
            educationDegrees.push(resumeEdu.degree);
        }
        if (Array.isArray(resumeEdu.degrees)) {
            educationDegrees.push(...resumeEdu.degrees);
        }
    }

    if (response.data && response.data.education && response.data.education.degree) {
        educationDegrees.push(response.data.education.degree);
    }

    let yearsExperience = 0;
    if (Array.isArray(response.experience) && response.experience.length) {
        const expEntry = response.experience[0];
        yearsExperience = expEntry.total_years || expEntry.years || 0;
    }

    if (response.resume_data && Array.isArray(response.resume_data.experience) && response.resume_data.experience.length) {
        const expEntry = response.resume_data.experience[0];
        yearsExperience = expEntry.total_years || expEntry.years || yearsExperience;
    }

    const interests = response.interests || (response.data && response.data.interests) || (response.resume_data && response.resume_data.interests) || [];

    const normalizedSkills = this.normalizeSkills(skills.join(', '));

    if (normalizedSkills.length === 0 && educationDegrees.length === 0 && !yearsExperience && interests.length === 0) {
        return null;
    }

    return {
        skills: normalizedSkills,
        interests: Array.isArray(interests) ? interests : this.normalizeSkills(String(interests)),
        education: { degrees: educationDegrees },
        experience: yearsExperience ? [{ years: yearsExperience }] : []
    };
};

DashboardModule.normalizeSkills = function(input) {
    if (!input) return [];
    return input
        .split(',')
        .map(item => item.trim())
        .filter(Boolean);
};

DashboardModule.submitProfileForAnalysis = function(profilePayload, userSkills) {
    this.showLoadingOverlay('Analyzing profile and matching roles...');

    fetch(this.config.apiEndpoints.analyzeProfile, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-Requested-With': 'XMLHttpRequest'
        },
        body: JSON.stringify(profilePayload)
    })
        .then(response => response.json())
        .then(data => {
            if (data.recommendations && data.recommendations.length) {
                this.renderRecommendations(data.recommendations, userSkills);
                this.setProfileStatus('Recommendations ready');
            } else {
                this.showAlert('warning', 'No recommendations returned. Try adding more skills.');
                this.showEmptyRecommendations();
            }
        })
        .catch(() => {
            this.showAlert('error', 'Profile analysis failed. Please try again.');
        })
        .finally(() => {
            this.hideLoadingOverlay();
        });
};

DashboardModule.renderRecommendations = function(recommendations, userSkills) {
    const list = document.getElementById('recommendationsList');
    const empty = document.getElementById('recommendationsEmpty');

    if (!list || !empty) return;

    const skillsLower = userSkills.map(skill => skill.toLowerCase());
    const aggregatedMissing = new Set();

    const cards = recommendations.slice(0, 3).map(rec => {
        const required = this.parseRequiredSkills(rec.required_skills);
        const matching = rec.matched_skills && rec.matched_skills.length ? rec.matched_skills : required.filter(skill => skillsLower.includes(skill.toLowerCase()));
        const missing = rec.missing_skills && rec.missing_skills.length ? rec.missing_skills : required.filter(skill => !skillsLower.includes(skill.toLowerCase()));
        const explanationLines = rec.explanation && rec.explanation.length ? rec.explanation : ['Calculated using skill overlap.'];

        missing.forEach(skill => aggregatedMissing.add(skill));

        const scoreValue = typeof rec.match_score === 'number'
            ? Math.round((rec.match_score <= 1 ? rec.match_score * 100 : rec.match_score))
            : 0;

        return `
            <article class="recommendation-card">
                <div class="d-flex align-items-start justify-content-between">
                    <div>
                        <h4>${rec.job_title || 'Career Role'}</h4>
                        <div class="match-score">
                            Match score <span class="score-pill">${scoreValue}%</span>
                        </div>
                    </div>
                    <i class="fas fa-briefcase text-primary"></i>
                </div>
                <div class="explanation-text">
                    ${explanationLines.map(line => `<div>${line}</div>`).join('')}
                </div>
                <div>
                    <div class="small text-muted">Matched skills</div>
                    <div class="tag-list">${matching.length ? matching.map(skill => `<span class="tag-item matching">${skill}</span>`).join('') : '<span class="empty-list">No matches yet</span>'}</div>
                </div>
                <div>
                    <div class="small text-muted">Missing skills</div>
                    <div class="tag-list">${missing.length ? missing.map(skill => `<span class="tag-item missing">${skill}</span>`).join('') : '<span class="empty-list">None identified</span>'}</div>
                </div>
                <div class="recommendation-actions">
                    <button class="btn btn-sm btn-outline-success" data-feedback="like" data-role="${rec.job_title || ''}">Relevant</button>
                    <button class="btn btn-sm btn-outline-secondary" data-feedback="dislike" data-role="${rec.job_title || ''}">Not relevant</button>
                </div>
            </article>
        `;
    }).join('');

    list.innerHTML = cards;
    list.classList.remove('d-none');
    empty.classList.add('d-none');

    this.updateSkillGapSummary(Array.from(aggregatedMissing));
    this.updateRoadmap(Array.from(aggregatedMissing));
    this.registerFeedbackHandlers();
};

DashboardModule.parseRequiredSkills = function(requiredSkills) {
    if (!requiredSkills) return [];
    if (Array.isArray(requiredSkills)) return requiredSkills;
    return String(requiredSkills)
        .split(',')
        .map(skill => skill.trim())
        .filter(Boolean);
};

DashboardModule.updateSkillGapSummary = function(missingSkills) {
    const container = document.getElementById('skillGapList');
    if (!container) return;

    if (!missingSkills.length) {
        container.textContent = 'No gaps calculated yet.';
        return;
    }

    container.innerHTML = missingSkills
        .slice(0, 10)
        .map(skill => `<span class="tag-item missing">${skill}</span>`)
        .join('');
};

DashboardModule.updateRoadmap = function(missingSkills) {
    const list = document.getElementById('roadmapList');
    if (!list) return;

    if (!missingSkills.length) {
        list.innerHTML = '<li>Complete a profile to generate a learning roadmap.</li>';
        return;
    }

    list.innerHTML = missingSkills.slice(0, 6)
        .map(skill => `<li>Learn ${skill} through a focused course and one practical project.</li>`)
        .join('');
};

DashboardModule.registerFeedbackHandlers = function() {
    const buttons = document.querySelectorAll('[data-feedback]');
    buttons.forEach(button => {
        button.addEventListener('click', () => {
            const role = button.getAttribute('data-role') || 'Role';
            const feedback = button.getAttribute('data-feedback');
            const label = feedback === 'like' ? 'Relevant' : 'Not relevant';

            this.submitFeedback({
                role: role,
                feedback: label
            });
        }, { once: true });
    });
};

DashboardModule.submitFeedback = function(payload) {
    fetch(this.config.apiEndpoints.feedback, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-Requested-With': 'XMLHttpRequest'
        },
        body: JSON.stringify(payload)
    })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                this.showAlert('error', data.error);
                return;
            }
            this.showAlert('success', 'Feedback saved.');
            this.loadFeedbackHistory();
        })
        .catch(() => {
            this.showAlert('error', 'Could not save feedback.');
        });
};

DashboardModule.loadFeedbackHistory = function() {
    const list = document.getElementById('feedbackList');
    if (!list) return;

    fetch(this.config.apiEndpoints.feedbackHistory)
        .then(response => response.json())
        .then(data => {
            if (!data.history || !data.history.length) {
                list.textContent = 'No feedback captured yet.';
                return;
            }
            list.innerHTML = data.history
                .map(item => {
                    const badgeClass = item.feedback === 'Relevant' ? 'success' : 'secondary';
                    return `
                        <div class="d-flex align-items-center justify-content-between mb-2">
                            <span>${item.role}</span>
                            <span class="badge bg-${badgeClass}">${item.feedback}</span>
                        </div>
                    `;
                })
                .join('');
        })
        .catch(() => {
            list.textContent = 'Unable to load feedback history.';
        });
};

DashboardModule.setProfileStatus = function(statusText) {
    const statusEl = document.getElementById('profileStatus');
    if (statusEl) {
        statusEl.textContent = statusText;
    }
};

DashboardModule.showEmptyRecommendations = function() {
    const list = document.getElementById('recommendationsList');
    const empty = document.getElementById('recommendationsEmpty');
    if (list) list.classList.add('d-none');
    if (empty) empty.classList.remove('d-none');
};

/**
 * ========================================
 * RECOMMENDATIONS SYSTEM
 * ========================================
 */
DashboardModule.getPersonalizedRecommendations = function() {
    if (!this.state.lastProfile) {
        this.showAlert('warning', 'Choose a resume or manual profile input first.');
        this.scrollToSection('input-modes');
        return;
    }

    this.submitProfileForAnalysis(this.state.lastProfile, this.state.lastSkills);
};

DashboardModule.loadRecommendations = function(analysis) {
    if (!analysis || !analysis.recommendations) {
        this.showEmptyRecommendations();
        return;
    }

    this.renderRecommendations(analysis.recommendations, this.state.lastSkills || []);
    this.state.hasRecommendations = true;
};

DashboardModule.explorecareers = function() {
    this.getPersonalizedRecommendations();
};
/**
 * ========================================
 * UI UTILITIES
 * ========================================
 */

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
    
    // Observe major panels
    document.querySelectorAll('.panel-card, .hero-panel, .recommendation-card, .empty-state').forEach(el => {
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
    this.state.currentUser = null;
};

window.DashboardModule = DashboardModule;