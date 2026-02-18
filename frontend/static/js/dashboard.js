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
        allowedFileTypes: ['pdf', 'doc', 'docx', 'txt'],
        apiEndpoints: {
            uploadResume: '/upload_resume',
            analyzeProfile: '/analyze_profile',
            feedback: '/feedback',
            feedbackHistory: '/api/feedback',
            liveJobs: '/api/jobs'
        }
    },
    
    // State
    state: {
        isUploading: false,
        hasRecommendations: false,
        currentUser: null,
        lastProfile: null,
        lastSkills: [],
        allRecommendations: [],
        currentFilters: {
            experience: '',
            workType: '',
            industry: '',
            matchScore: 0,
            location: ''
        }
    },
    
    // Initialize dashboard
    init: function() {
        this.setupEventListeners();
        this.initializeFileUpload();
        this.setupScrollAnimations();
        this.loadUserData();
        this.loadFeedbackHistory();
    }
};

DashboardModule.getCsrfToken = function() {
    return document.querySelector('meta[name="csrf-token"]')?.content || '';
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
    
    // Filter events
    this.setupFilterEvents();
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
    
    // Re-run Analysis button
    document.getElementById('rerunAnalysisBtn')?.addEventListener('click', () => {
        if (this.state.lastProfile) {
            this.submitProfileForAnalysis(this.state.lastProfile, this.state.lastSkills);
        }
    });
};

DashboardModule.setupFilterEvents = function() {
    const filterInputs = ['filterExperience', 'filterWorkType', 'filterIndustry', 'filterMatchScore', 'filterLocation'];
    const clearBtn = document.getElementById('clearFiltersBtn');
    
    filterInputs.forEach(inputId => {
        document.getElementById(inputId)?.addEventListener('change', () => {
            this.applyFilters();
        });
        document.getElementById(inputId)?.addEventListener('input', () => {
            this.applyFilters();
        });
    });
    
    clearBtn?.addEventListener('click', () => {
        filterInputs.forEach(inputId => {
            const el = document.getElementById(inputId);
            if (el) {
                if (inputId === 'filterMatchScore') {
                    el.value = '0';
                } else {
                    el.value = '';
                }
            }
        });
        this.applyFilters();
    });
};

DashboardModule.applyFilters = function() {
    // Get filter values
    this.state.currentFilters = {
        experience: document.getElementById('filterExperience')?.value || '',
        workType: document.getElementById('filterWorkType')?.value || '',
        industry: document.getElementById('filterIndustry')?.value || '',
        matchScore: parseInt(document.getElementById('filterMatchScore')?.value || 0),
        location: document.getElementById('filterLocation')?.value?.toLowerCase() || ''
    };
    
    // Filter recommendations
    let filtered = this.state.allRecommendations || [];
    
    if (this.state.currentFilters.experience) {
        filtered = filtered.filter(rec => {
            return (rec.experience_level || '').toLowerCase() === this.state.currentFilters.experience.toLowerCase();
        });
    }
    
    if (this.state.currentFilters.matchScore > 0) {
        filtered = filtered.filter(rec => {
            const score = typeof rec.match_score === 'number' ? (rec.match_score <= 1 ? rec.match_score * 100 : rec.match_score) : 0;
            return score >= this.state.currentFilters.matchScore;
        });
    }
    
    // Re-render with filtered results
    this.renderRecommendations(filtered, this.state.lastSkills || []);
    
    // Show filter indicator
    const hasActiveFilters = Object.values(this.state.currentFilters).some(v => v !== '' && v !== 0);
    const filterIndicator = document.querySelector('[id="filterPanel"]');
    if (hasActiveFilters && filterIndicator) {
        filterIndicator.style.borderLeft = '3px solid #007bff';
    }
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
            message: 'Please upload a PDF, DOC, DOCX, or TXT file'
        };
    }
    
    return { valid: true };
};

DashboardModule.uploadResumeFile = async function(formData) {
    try {
        const csrfToken = this.getCsrfToken();
        const response = await fetch(this.config.apiEndpoints.uploadResume, {
            method: 'POST',
            body: formData,
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                ...(csrfToken ? { 'X-CSRFToken': csrfToken } : {})
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
    this.state.lastProfile = profilePayload;
    this.state.lastSkills = profilePayload.skills || [];
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

    // Update profile completion bar
    this.updateProfileCompletion(profilePayload);

    const csrfToken = this.getCsrfToken();

    fetch(this.config.apiEndpoints.analyzeProfile, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-Requested-With': 'XMLHttpRequest',
            ...(csrfToken ? { 'X-CSRFToken': csrfToken } : {})
        },
        body: JSON.stringify(profilePayload)
    })
        .then(response => response.json())
        .then(data => {
            // Profile analysis completed
            
            // Always render recommendations if available (even 0% matches are useful)
            if (data.recommendations && data.recommendations.length) {
                this.renderRecommendations(data.recommendations, userSkills);
                this.setProfileStatus('Recommendations ready');
            } else {
                this.showAlert('warning', 'No recommendations returned. Try adding skills.');
                this.showEmptyRecommendations();
            }

            // Always display real market skills from Adzuna API - highest priority
            if (data.market_skills && Object.keys(data.market_skills).length > 0) {
                this.updateSkillGapSummaryWithMarketData(data.market_skills);
                this.updateRoadmapWithMarketData(data.market_skills, userSkills);
            } else {
                console.warn('✗ No market skills in response');
                this.updateSkillGapSummary([]);
                this.updateRoadmap([]);
            }

            // Load live jobs based on profile
            this.loadLiveJobs(profilePayload, userSkills);
        })
        .catch(error => {
            console.error('Profile analysis error:', error);
            this.showAlert('error', 'Profile analysis failed. Please try again.');
        })
        .finally(() => {
            this.hideLoadingOverlay();
        });
};

DashboardModule.buildLiveQuery = function(profilePayload, userSkills) {
    const skills = userSkills || [];
    const interests = (profilePayload && profilePayload.interests) || [];
    
    // Prioritize technical skills that appear in job listings
    const highValueSkills = ['python', 'java', 'javascript', 'react', 'node', 'aws', 'docker', 
                             'kubernetes', 'machine learning', 'ai', 'data science', 'sql', 
                             'angular', 'vue', 'typescript', 'go', 'rust', 'c++', 'c#', '.net'];
    
    // Filter user skills to prioritize high-value ones
    const prioritySkills = skills.filter(skill => 
        highValueSkills.some(hvSkill => skill.toLowerCase().includes(hvSkill))
    );
    
    // Build query from top 2-3 relevant skills
    let querySkills = prioritySkills.length >= 2 
        ? prioritySkills.slice(0, 3) 
        : skills.slice(0, 3);
    
    // If we have interests, combine with top skill
    if (querySkills.length && interests.length) {
        return `${querySkills[0]} ${interests[0]}`;
    }
    
    // Use skills if available
    if (querySkills.length) {
        return querySkills.slice(0, 2).join(' ');
    }
    
    // Fall back to interests
    if (interests.length) {
        return interests.slice(0, 2).join(' ');
    }
    
    return 'software developer';
};

DashboardModule.loadLiveJobs = function(profilePayload, userSkills) {
    const list = document.getElementById('liveJobsList');
    const empty = document.getElementById('liveJobsEmpty');
    if (!list || !empty) return;

    const query = this.buildLiveQuery(profilePayload, userSkills);
    const params = new URLSearchParams({ query: query, location: 'India', results: 6 });

    fetch(`${this.config.apiEndpoints.liveJobs}?${params.toString()}`)
        .then(response => response.json())
        .then(data => {
            const jobs = (data && data.live_jobs && data.live_jobs.length)
                ? data.live_jobs
                : (data && data.jobs && data.jobs.length ? data.jobs : []);

            if (!jobs.length) {
                list.classList.add('d-none');
                empty.classList.remove('d-none');
                return;
            }

            const cards = jobs.map(job => {
                const salary = job.salary_min || job.salary_max
                    ? `$${job.salary_min || ''} - $${job.salary_max || ''}`
                    : 'Salary not listed';

                return `
                    <article class="recommendation-card">
                        <div class="d-flex align-items-start justify-content-between">
                            <div>
                                <h4>${job.job_title || 'Job Role'}</h4>
                                <div class="match-score">${job.company || 'Company'}</div>
                            </div>
                            <i class="fas fa-briefcase text-primary"></i>
                        </div>
                        <div class="explanation-text">
                            <div><i class="fas fa-map-marker-alt me-1"></i>${job.location || 'Location'}</div>
                            <div><i class="fas fa-dollar-sign me-1"></i>${salary}</div>
                        </div>
                        <div class="recommendation-actions">
                            <a class="btn btn-sm btn-outline-primary" href="${job.redirect_url || '#'}" target="_blank" rel="noopener">
                                <i class="fas fa-external-link-alt me-1"></i>View job
                            </a>
                        </div>
                    </article>
                `;
            }).join('');

            list.innerHTML = cards;
            list.classList.remove('d-none');
            empty.classList.add('d-none');
            
            // Update data source timestamp
            this.updateDataSourceTimestamp();
        })
        .catch(() => {
            list.classList.add('d-none');
            empty.classList.remove('d-none');
        });
};

DashboardModule.updateDataSourceTimestamp = function() {
    const timestampEl = document.getElementById('dataLastUpdated');
    if (timestampEl) {
        const now = new Date();
        const hours = String(now.getHours()).padStart(2, '0');
        const minutes = String(now.getMinutes()).padStart(2, '0');
        timestampEl.textContent = `• Last refreshed: ${hours}:${minutes}`;
    }
};

DashboardModule.renderRecommendations = function(recommendations, userSkills) {
    const list = document.getElementById('recommendationsList');
    const empty = document.getElementById('recommendationsEmpty');

    if (!list || !empty) return;

    const skillsLower = userSkills.map(skill => skill.toLowerCase());
    const aggregatedMissing = new Set();

    // Show only suitable matches (40%+) to avoid overwhelming with low-quality results
    // This filters out the many 25% matches and shows only relevant careers
    const suitableRecs = recommendations.filter(rec => {
        const score = typeof rec.match_score === 'number' 
            ? (rec.match_score <= 1 ? rec.match_score * 100 : rec.match_score)
            : 0;
        return score >= 40;
    });
    
    // If no suitable matches found, show top 3 for awareness
    const allRecs = suitableRecs.length > 0 ? suitableRecs : recommendations.slice(0, 3);

    const cards = allRecs.map((rec, index) => {
        const required = this.parseRequiredSkills(rec.required_skills);
        const matching = rec.matched_skills && rec.matched_skills.length ? rec.matched_skills : required.filter(skill => skillsLower.includes(skill.toLowerCase()));
        const missing = rec.missing_skills && rec.missing_skills.length ? rec.missing_skills : required.filter(skill => !skillsLower.includes(skill.toLowerCase()));
        const explanationLines = rec.explanation && rec.explanation.length ? rec.explanation : ['Calculated using skill overlap.'];

        missing.forEach(skill => aggregatedMissing.add(skill));

        const scoreValue = typeof rec.match_score === 'number'
            ? Math.round((rec.match_score <= 1 ? rec.match_score * 100 : rec.match_score))
            : 0;
        
        // Generate unique ID for expandable section
        const explainId = `explain-${index}-${Date.now()}`;

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
                <div style="margin-top: 12px; padding-top: 12px; border-top: 1px solid #e0e0e0;">
                    <button class="btn btn-sm btn-link p-0 text-primary" data-bs-toggle="collapse" href="#${explainId}" role="button" aria-expanded="false" aria-controls="${explainId}">
                        <i class="fas fa-info-circle me-1"></i>View explanation
                    </button>
                    <div class="collapse mt-3" id="${explainId}">
                        <div class="alert alert-info" style="margin-bottom: 0;">
                            <strong>Why ${scoreValue}%?</strong>
                            <ul style="margin: 8px 0 0 20px; padding: 0;">
                                <li>${matching.length}/${required.length} required skills matched</li>
                                <li>${missing.length} skills to prioritize learning</li>
                                <li>${explanationLines[0] || 'Based on your profile match'}</li>
                            </ul>
                        </div>
                    </div>
                </div>
                <div style="margin-top: 12px;">
                    <div class="small text-muted">Matched skills
                        <span style="color: #666; font-weight: normal; margin-left: 8px;">
                            ${rec.skill_confidence ? '(' + Object.values(rec.skill_confidence)[0] + ')' : ''}
                        </span>
                    </div>
                    <div class="tag-list">
                        ${matching.length ? matching.map(skill => {
                            const confidence = rec.skill_confidence && rec.skill_confidence[skill] ? rec.skill_confidence[skill] : 'Intermediate';
                            const confidenceColor = confidence === 'Advanced' ? '#28a745' : confidence === 'Intermediate' ? '#ffc107' : '#6c757d';
                            return `<span class="tag-item matching" style="border-left: 3px solid ${confidenceColor}" title="${confidence} level">
                                ${skill} <small style="color: #666; margin-left: 4px;">[${confidence}]</small>
                            </span>`;
                        }).join('') : '<span class="empty-list">No matches yet</span>'}
                    </div>
                </div>
                <div style="margin-top: 10px;">
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
    
    // Store all recommendations for filtering
    this.state.allRecommendations = allRecs;
    
    // Show filter panel now that we have results
    const filterPanel = document.getElementById('filterPanel');
    if (filterPanel) {
        filterPanel.classList.remove('d-none');
    }
    
    // Show "Re-run Analysis" button now that we have results
    const rerunBtn = document.getElementById('rerunAnalysisBtn');
    if (rerunBtn) {
        rerunBtn.style.display = 'inline-block';
    }

    // Don't overwrite skill gap and roadmap - they're now from market_skills in submitProfileForAnalysis
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

/**
 * Display real market skills from Adzuna API with demand frequency
 */
DashboardModule.updateSkillGapSummaryWithMarketData = function(marketSkills) {
    const container = document.getElementById('skillGapList');
    if (!container) return;

    // Always show container, even if no market skills (will show message)
    container.classList.remove('empty-list');

    if (!marketSkills || Object.keys(marketSkills).length === 0) {
        container.innerHTML = '<div class="alert alert-info">Analyzing market data...</div>';
        return;
    }

    // Sort by frequency (demand) - highest demand first
    const skillsWithFreq = Object.entries(marketSkills)
        .map(([skill, frequency]) => ({ skill, frequency }))
        .sort((a, b) => b.frequency - a.frequency)
        .slice(0, 15);  // Show more skills

    // Create tags with demand indicators
    const skillsHtml = skillsWithFreq
        .map(({ skill, frequency }) => {
            // Adjusted thresholds for realistic sample sizes (15 jobs)
            // 10+ = 66% of jobs = High demand | 6-9 = 40-60% = Medium | <6 = Emerging  
            const demandLevel = frequency >= 10 ? 'high' : frequency >= 6 ? 'medium' : 'low';
            const demandIcon = frequency >= 10 ? '🔴' : frequency >= 6 ? '🟡' : '🟢';
            const title = `Appears in ${frequency} real job listings from Adzuna API`;
            
            return `<span class="tag-item market-skill" title="${title}" data-demand="${demandLevel}">
                <strong>${skill}</strong>
                <span style="font-size: 0.8em; margin-left: 6px; opacity: 0.8;">${demandIcon} ${frequency}</span>
            </span>`;
        })
        .join('');

    container.innerHTML = `<div class="market-skills-container">
        <div class="mb-2" style="font-size: 0.9em; color: #059669;">
            <i class="fas fa-chart-line me-1"></i>Real market demand from Indian job market
        </div>
        ${skillsHtml}
    </div>`;
};

/**
 * Display real learning roadmap from market demand
 */
DashboardModule.updateRoadmapWithMarketData = function(marketSkills, userSkills) {
    const list = document.getElementById('roadmapList');
    if (!list) return;

    if (!marketSkills || Object.keys(marketSkills).length === 0) {
        list.innerHTML = '<li><em>Fetching real market data...</em></li>';
        return;
    }

    // Get user skills in lowercase for comparison
    const userSkillsLower = (userSkills || []).map(s => s.toLowerCase());

    // Sort market skills by demand (frequency)
    const sortedSkills = Object.entries(marketSkills)
        .map(([skill, frequency]) => ({ skill, frequency }))
        .sort((a, b) => b.frequency - a.frequency)
        .slice(0, 8);

    if (sortedSkills.length === 0) {
        list.innerHTML = '<li>No market skills identified.</li>';
        return;
    }

    // Separate into existing and new skills
    const existingSkills = [];
    const newSkills = [];

    sortedSkills.forEach(({ skill, frequency }) => {
        const hasSkill = userSkillsLower.some(us => us.includes(skill.toLowerCase()) || skill.toLowerCase().includes(us));
        if (hasSkill) {
            existingSkills.push({ skill, frequency });
        } else {
            newSkills.push({ skill, frequency });
        }
    });

    // Build HTML
    let roadmapHtml = '';

    // Section 1: Skills you already have (strengthen these)
    if (existingSkills.length > 0) {
        roadmapHtml += `<li style="list-style: none; font-weight: 600; color: #059669; margin-bottom: 0.5rem;">
            <i class="fas fa-check-circle me-1"></i>Strengthen These (You Have)
        </li>`;
        roadmapHtml += existingSkills
            .map(({ skill, frequency }) => {
                const jobCount = frequency > 100 ? '100+' : frequency;
                const demandBadge = frequency >= 10 ? '🔴 High' : frequency >= 6 ? '🟡 Medium' : '🟢 Good';
                return `<li style="margin-left: 1.5rem; margin-bottom: 0.3rem;">
                    <strong>${skill}</strong> <span style="font-size: 0.85em; color: #059669;">${demandBadge} demand (${jobCount} jobs)</span>
                    <br><small style="color: #6b7280;">Advanced projects to deepen expertise</small>
                </li>`;
            })
            .join('');
    }

    // Section 2: Skills to learn (priority learning path)
    if (newSkills.length > 0) {
        if (existingSkills.length > 0) {
            roadmapHtml += `<li style="list-style: none; font-weight: 600; color: #3b82f6; margin-top: 1rem; margin-bottom: 0.5rem;">
                <i class="fas fa-graduation-cap me-1"></i>Learn These (Priority Order)
            </li>`;
        }
        roadmapHtml += newSkills
            .map(({ skill, frequency }, index) => {
                const jobCount = frequency > 100 ? '100+' : frequency;
                const demandBadge = frequency >= 10 ? '🔴 High' : frequency >= 6 ? '🟡 Medium' : '🟢 Good';
                return `<li style="margin-left: 1.5rem; margin-bottom: 0.3rem;">
                    <strong>${index + 1}. ${skill}</strong> <span style="font-size: 0.85em; color: #3b82f6;">${demandBadge} demand (${jobCount} jobs)</span>
                    <br><small style="color: #6b7280;">Online courses → Real projects → GitHub → Job applications</small>
                </li>`;
            })
            .join('');
    }

    list.innerHTML = roadmapHtml;
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
    const csrfToken = this.getCsrfToken();

    fetch(this.config.apiEndpoints.feedback, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-Requested-With': 'XMLHttpRequest',
            ...(csrfToken ? { 'X-CSRFToken': csrfToken } : {})
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
            // Auto-refresh feedback history in real-time
            setTimeout(() => this.loadFeedbackHistory(), 300);
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
                    const deleteBtn = `<button class="btn btn-sm btn-outline-danger delete-feedback" data-feedback-id="${item.id}" title="Delete this feedback"><i class="fas fa-trash-alt"></i></button>`;
                    return `
                        <div class="d-flex align-items-center justify-content-between mb-2 p-2 border rounded">
                            <div>
                                <strong>${item.role}</strong>
                                <span class="ms-2 badge bg-${badgeClass}">${item.feedback}</span>
                                <div class="small text-muted">${new Date(item.created_at).toLocaleDateString()}</div>
                            </div>
                            ${deleteBtn}
                        </div>
                    `;
                })
                .join('');
            
            // Bind delete handlers
            this.bindDeleteFeedbackHandlers();
        })
        .catch(() => {
            list.textContent = 'Unable to load feedback history.';
        });
};

DashboardModule.bindDeleteFeedbackHandlers = function() {
    const deleteButtons = document.querySelectorAll('.delete-feedback');
    deleteButtons.forEach(button => {
        button.addEventListener('click', (e) => {
            e.preventDefault();
            const feedbackId = button.getAttribute('data-feedback-id');
            this.deleteFeedback(feedbackId);
        });
    });
};

DashboardModule.deleteFeedback = function(feedbackId) {
    if (!confirm('Are you sure you want to delete this feedback?')) return;
    
    const csrfToken = this.getCsrfToken();
    
    fetch(`/api/feedback/${feedbackId}`, {
        method: 'DELETE',
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
            ...(csrfToken ? { 'X-CSRFToken': csrfToken } : {})
        }
    })
        .then(response => {
            if (!response.ok) throw new Error('Delete failed');
            return response.json();
        })
        .then(data => {
            this.showAlert('success', 'Feedback deleted successfully');
            // Reload feedback history
            setTimeout(() => this.loadFeedbackHistory(), 500);
        })
        .catch(() => {
            this.showAlert('error', 'Could not delete feedback.');
        });
};

DashboardModule.setProfileStatus = function(statusText) {
    const statusEl = document.getElementById('profileStatus');
    if (statusEl) {
        statusEl.textContent = statusText;
    }
};

DashboardModule.updateProfileCompletion = function(profile) {
    // Calculate profile completion percentage
    let completionScore = 0;
    const totalComponents = 5;
    
    // Check resume upload (20%)
    if (profile && profile.resume_text && profile.resume_text.length > 10) {
        completionScore += 1;
    }
    
    // Check skills (20%)
    if (profile && profile.skills && profile.skills.length > 0) {
        completionScore += 1;
    }
    
    // Check education (20%)
    if (profile && profile.education && profile.education.degree && profile.education.degree.length > 0) {
        completionScore += 1;
    }
    
    // Check experience (20%)
    if (profile && profile.experience && profile.experience.length > 0) {
        completionScore += 1;
    }
    
    // Check interests (20%)
    if (profile && profile.interests && profile.interests.length > 0) {
        completionScore += 1;
    }
    
    // Calculate percentage
    const completionPercent = Math.round((completionScore / totalComponents) * 100);
    
    // Update UI
    const progressBar = document.getElementById('profileProgressBar');
    const completionText = document.getElementById('profileCompletionText');
    
    if (progressBar) {
        progressBar.style.width = completionPercent + '%';
        progressBar.setAttribute('aria-valuenow', completionPercent);
    }
    
    if (completionText) {
        completionText.textContent = completionPercent + '% complete';
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