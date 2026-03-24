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
            currentProfile: '/api/profile/current',
            clearProfile: '/api/profile/current',
            feedback: '/feedback',
            feedbackHistory: '/api/feedback',
            liveJobs: '/api/jobs',
            speechProfileExtract: '/api/speech/profile-extract',
            aiInterviewQuestion: '/api/ai/interview-question',
            aiInterviewEvaluate: '/api/ai/interview-evaluate'
        }
    },
    
    // State
    state: {
        isUploading: false,
        hasRecommendations: false,
        hasSessionInput: false,
        currentUser: null,
        lastProfile: null,
        lastSkills: [],
        lastSkillGap: [],
        allRecommendationsRaw: [],
        allRecommendations: [],
        allLiveJobs: [],
        liveJobsSource: 'adzuna',
        currentFilters: {
            experience: '',
            workType: '',
            industry: '',
            matchScore: 0,
            location: '',
            salaryMin: 0
        }
    },
    
    // Initialize dashboard
    init: function() {
        this.setupEventListeners();
        this.initializeFileUpload();
        this.setupScrollAnimations();
        this.loadUserData();
        this.showOnboardingTooltip();
        this.setupThemeToggleIcon();
        this.loadAISuggestions();
        this.loadSkillGapAnalytics();
        this.loadExplainableOutput();
        this.loadSkillDemandAnalytics();
        this.loadAIInsightBox();
        this.setupLiveJobsFallback();
        this.loadFeedbackHistory();
        this.resetLiveJobsPanel({
            title: 'Live Jobs Not Loaded',
            subtitle: 'Complete your profile and run matching to load relevant live jobs.'
        });
    },

    // Always show spinner and fallback for Live Jobs
    setupLiveJobsFallback: function() {
                                    const liveJobsContent = document.getElementById('live-jobs-content');
                                    const spinner = document.getElementById('live-jobs-spinner');
                                    const message = document.getElementById('live-jobs-message');
                                    if (!liveJobsContent || !spinner || !message) return;
                                    // Show spinner on load
                                    spinner.style.display = 'inline-block';
                                    message.textContent = 'Loading live jobs...';
                                    // Hide spinner after jobs load or fail (hook into renderLiveJobs and resetLiveJobsPanel)
                                    const origRender = this.renderLiveJobs.bind(this);
                                    this.renderLiveJobs = function(jobs, source = 'adzuna', options = {}) {
                                        spinner.style.display = 'none';
                                        message.style.display = 'none';
                                        origRender(jobs, source, options);
                                    };
                                    const origReset = this.resetLiveJobsPanel.bind(this);
                                    this.resetLiveJobsPanel = function(options = {}) {
                                        spinner.style.display = 'none';
                                        message.style.display = 'block';
                                        message.textContent = options && options.subtitle ? options.subtitle : 'Live job data unavailable. Please refresh or try again later.';
                                        origReset(options);
                                    };
                                },
                            // Load AI Insight Box (hero section)
                            loadAIInsightBox: function() {
                                const insightBox = document.getElementById('ai-insight-content');
                                if (!insightBox) return;
                                insightBox.innerHTML = 'Loading your AI insights...';
                                fetch('/api/profile/current', {
                                    method: 'GET',
                                    headers: {
                                        'X-CSRFToken': this.getCsrfToken(),
                                        'Accept': 'application/json'
                                    }
                                })
                                .then(res => res.json())
                                .then(data => {
                                    if (!data.has_profile || !data.profile) {
                                        insightBox.innerHTML = 'Upload your resume to see your best job matches, missing skills, and readiness estimate.';
                                        return;
                                    }
                                    fetch('/analyze_profile', {
                                        method: 'POST',
                                        headers: {
                                            'Content-Type': 'application/json',
                                            'X-CSRFToken': this.getCsrfToken(),
                                            'Accept': 'application/json'
                                        },
                                        body: JSON.stringify(data.profile)
                                    })
                                    .then(res => res.json())
                                    .then(result => {
                                        let html = '';
                                        if (result.recommendations && result.recommendations.length > 0) {
                                            const top = result.recommendations[0];
                                            html += `<div><span class='fw-bold text-primary'><i class='fas fa-star me-1'></i>Top Match:</span> ${top.job_title} <span class='badge bg-primary ms-2'>${top.match_score}%</span></div>`;
                                            if (top.confidence_band) {
                                                html += ` <span class='badge bg-info text-dark ms-1'>${top.confidence_band}</span>`;
                                            }
                                            if (top.explanation && top.explanation.length) {
                                                html += `<div class='small text-muted mt-1'>${top.explanation[0]}</div>`;
                                            }
                                        } else {
                                            html += `<div>No matches yet. Add more skills or interests for better results.</div>`;
                                        }
                                        if (result.skill_gap && result.skill_gap.length > 0) {
                                            html += `<div class='mt-2'><span class='fw-bold text-warning'><i class='fas fa-exclamation-circle me-1'></i>Skill Gap:</span> ${result.skill_gap.slice(0,3).join(', ')}${result.skill_gap.length > 3 ? ', ...' : ''}</div>`;
                                        } else if (result.skill_gap && result.skill_gap.length === 0) {
                                            html += `<div class='mt-2 text-success'><i class='fas fa-check-circle me-1'></i>No major skill gaps detected.</div>`;
                                        }
                                        if (result.readiness !== undefined) {
                                            html += `<div class='mt-2'><span class='fw-bold text-success'><i class='fas fa-bolt me-1'></i>Readiness:</span> ${result.readiness}%</div>`;
                                        }
                                        insightBox.innerHTML = html;
                                    })
                                    .catch(() => {
                                        insightBox.innerHTML = 'Could not load AI insights. Try again later.';
                                    });
                                })
                                .catch(() => {
                                    insightBox.innerHTML = 'Could not load AI insights. Try again later.';
                                });
                            },
                        // Load Explainable Output
                        loadExplainableOutput: function() {
                            const panel = document.getElementById('explainableOutputPanel');
                            if (!panel) return;
                            fetch('/api/recommendations', {
                                method: 'GET',
                                headers: {
                                    'X-CSRFToken': this.getCsrfToken(),
                                    'Accept': 'application/json'
                                }
                            })
                            .then(res => res.json())
                            .then(data => {
                                if (!data.explanations) {
                                    panel.innerHTML = '<div class="text-muted">No explainable output available. Run analysis to see details.</div>';
                                    return;
                                }
                                let html = '';
                                Object.entries(data.explanations).forEach(([job, exp]) => {
                                    html += `<div class="explainable-card mb-3">
                                        <h5>${job}</h5>
                                        <div><strong>Why recommended:</strong> ${exp.why_recommended}</div>
                                        <div><strong>Matched skills:</strong> ${exp.skill_analysis.matching.join(', ') || '--'}</div>
                                        <div><strong>Missing skills:</strong> ${exp.skill_analysis.gaps.join(', ') || '--'}</div>
                                        <div><strong>Confidence:</strong> ${exp.growth_opportunities.potential || '--'}</div>
                                        <div><strong>Improvement suggestions:</strong> ${exp.improvement_suggestions.join(', ')}</div>
                                    </div>`;
                                });
                                panel.innerHTML = html;
                            })
                            .catch(() => {
                                panel.innerHTML = '<div class="text-danger">Failed to load explainable output. Try again later.</div>';
                            });
                        },

                        // Load Skill Demand Analytics
                        loadSkillDemandAnalytics: function() {
                            const panel = document.getElementById('skillDemandPanel');
                            if (!panel) return;
                            fetch('/api/profile/current', {
                                method: 'GET',
                                headers: {
                                    'X-CSRFToken': this.getCsrfToken(),
                                    'Accept': 'application/json'
                                }
                            })
                            .then(res => res.json())
                            .then(data => {
                                if (!data.has_profile || !data.profile) {
                                    panel.innerHTML = `<div class="empty-state text-center py-4">
                                        <i class="fas fa-user-circle fa-3x text-secondary mb-3"></i>
                                        <h6 class="mb-2">No Profile Found</h6>
                                        <p class="mb-3">Upload your resume or build your profile to unlock analytics and personalized insights.</p>
                                        <button class="btn btn-primary" onclick="document.getElementById('uploadResumeNav').click()">
                                            <i class="fas fa-file-upload me-2"></i>Upload Resume
                                        </button>
                                        <button class="btn btn-outline-secondary ms-2" onclick="document.getElementById('manualProfileNav').click()">
                                            <i class="fas fa-edit me-2"></i>Build Profile
                                        </button>
                                    </div>`;
                                    return;
                                }
                                let completion = 0;
                                if (data.profile.education && data.profile.education.degrees && data.profile.education.degrees.length) completion += 25;
                                if (data.profile.experience && data.profile.experience.length && data.profile.experience[0].years > 0) completion += 25;
                                if (data.profile.skills && data.profile.skills.length) completion += 35;
                                if (data.profile.interests && data.profile.interests.length) completion += 15;
                                completion = Math.min(100, completion);
                                // Summary card
                                let summary = `<div class="dashboard-card mb-3" style="display:flex;align-items:center;gap:18px;">
                                    <div style="flex:1;">
                                        <div class="fw-bold mb-1">Profile Completion</div>
                                        <div class="progress mb-1" style="height: 10px;">
                                            <div class="progress-bar bg-success" role="progressbar" style="width: ${completion}%" aria-valuenow="${completion}" aria-valuemin="0" aria-valuemax="100"></div>
                                        </div>
                                        <span class="badge bg-success fs-6">${completion}%</span>
                                    </div>
                                    <div style="flex:1;">
                                        <div class="small text-muted">Education, experience, skills, and interests contribute to completion.</div>
                                    </div>
                                </div>`;
                                panel.innerHTML = summary;
                            })
                            .catch(() => {
                                panel.innerHTML = '<div class="text-danger">Failed to load profile analytics. Try again later.</div>';
                            });
                        },

                        // Load Skill Gap Analytics
                    loadSkillGapAnalytics: function() {
                        const panel = document.getElementById('skill-gap-analytics-content');
                        if (!panel) return;
                        fetch('/api/profile/current', {
                            method: 'GET',
                            headers: {
                                'X-CSRFToken': this.getCsrfToken(),
                                'Accept': 'application/json'
                            }
                        })
                        .then(res => res.json())
                        .then(data => {
                            if (!data.has_profile || !data.profile) {
                                panel.innerHTML = `
                                    <div class="empty-state text-center py-4">
                                        <i class="fas fa-chart-bar fa-3x text-secondary mb-3"></i>
                                        <h6 class="mb-2">No Profile Found</h6>
                                        <p class="mb-3">Upload your resume or build your profile to view skill gap insights.</p>
                                        <button class="btn btn-primary" onclick="document.getElementById('uploadResumeNav').click()">
                                            <i class="fas fa-file-upload me-2"></i>Upload Resume
                                        </button>
                                        <button class="btn btn-outline-secondary ms-2" onclick="document.getElementById('manualProfileNav').click()">
                                            <i class="fas fa-edit me-2"></i>Build Profile
                                        </button>
                                    </div>`;
                                return;
                            }
                            fetch('/analyze_profile', {
                                method: 'POST',
                                headers: {
                                    'Content-Type': 'application/json',
                                    'X-CSRFToken': this.getCsrfToken(),
                                    'Accept': 'application/json'
                                },
                                body: JSON.stringify(data.profile)
                            })
                            .then(res => res.json())
                            .then(result => {
                                if (!result.skill_gap || result.skill_gap.length === 0) {
                                    panel.innerHTML = '<div class="dashboard-card bg-success bg-opacity-10 text-success mb-2"><i class="fas fa-check-circle me-2"></i>No skill gaps detected. Your profile covers all key areas.</div>';
                                    return;
                                }
                                let html = '<div class="dashboard-card mb-2"><div class="fw-bold mb-2">Top Skill Gaps</div><ul class="list-group">';
                                result.skill_gap.forEach(skill => {
                                    html += `<li class="list-group-item d-flex align-items-center"><span class="badge bg-warning text-dark me-2"><i class="fas fa-exclamation-circle"></i></span>${skill}</li>`;
                                });
                                html += '</ul></div>';
                                panel.innerHTML = html;
                            })
                            .catch(() => {
                                panel.innerHTML = '<div class="text-danger">Failed to load skill gap insights. Try again later.</div>';
                            });
                        })
                        .catch(() => {
                            panel.innerHTML = '<div class="text-danger">Failed to load profile. Try again later.</div>';
                        });
                    },
                // Load AI Suggestions
                loadAISuggestions: function() {
                    const panel = document.getElementById('ai-suggestions-content');
                    if (!panel) return;
                    fetch('/api/profile/current', {
                        method: 'GET',
                        headers: {
                            'X-CSRFToken': this.getCsrfToken(),
                            'Accept': 'application/json'
                        }
                    })
                        .then(res => res.json())
                        .then(data => {
                            if (!data.has_profile || !data.profile) {
                                panel.innerHTML = `
                                    <div class="empty-state text-center py-4">
                                        <i class="fas fa-robot fa-3x text-secondary mb-3"></i>
                                        <h6 class="mb-2">No Profile Found</h6>
                                        <p class="mb-3">Upload your resume or build your profile to get AI-powered career suggestions.</p>
                                        <button class="btn btn-primary" onclick="document.getElementById('uploadResumeNav').click()">
                                            <i class="fas fa-file-upload me-2"></i>Upload Resume
                                        </button>
                                        <button class="btn btn-outline-secondary ms-2" onclick="document.getElementById('manualProfileNav').click()">
                                            <i class="fas fa-edit me-2"></i>Build Profile
                                        </button>
                                    </div>`;
                                return;
                            }
                            fetch('/analyze_profile', {
                                method: 'POST',
                                headers: {
                                    'Content-Type': 'application/json',
                                    'X-CSRFToken': this.getCsrfToken(),
                                    'Accept': 'application/json'
                                },
                                body: JSON.stringify(data.profile)
                            })
                            .then(res => res.json())
                            .then(result => {
                                if (!result.recommendations || result.recommendations.length === 0) {
                                    panel.innerHTML = '<div class="dashboard-card bg-warning bg-opacity-10 text-warning mb-2"><i class="fas fa-info-circle me-2"></i>No recommendations found. Add more skills or interests for better matches.</div>';
                                    return;
                                }
                                let html = '<div class="dashboard-card mb-2"><div class="fw-bold mb-2">Top Career Recommendations</div><ul class="list-group">';
                                result.recommendations.forEach(rec => {
                                    html += `<li class="list-group-item d-flex flex-column flex-md-row align-items-md-center justify-content-between">
                                        <div class="fw-bold"><i class="fas fa-briefcase me-2"></i>${rec.job_title}</div>
                                        <div class="d-flex align-items-center gap-2 mt-1 mt-md-0">
                                            <span class="badge bg-primary">${rec.match_score}% Match</span>
                                            <span class="badge bg-info text-dark">${rec.confidence_band}</span>
                                        </div>
                                        <div class="mt-1 small text-muted">${rec.explanation.join('<br>')}</div>
                                    </li>`;
                                });
                                html += '</ul></div>';
                                panel.innerHTML = html;
                            })
                            .catch(() => {
                                panel.innerHTML = '<div class="text-danger">Failed to load AI suggestions. Try again later.</div>';
                            });
                        })
                        .catch(() => {
                            panel.innerHTML = '<div class="text-danger">Failed to load profile. Try again later.</div>';
                        });
                },
            // Show onboarding tooltip
            showOnboardingTooltip: function() {
                const tooltip = document.getElementById('onboarding-tooltip');
                if (tooltip) {
                    setTimeout(() => {
                        tooltip.style.display = 'block';
                    }, 800);
                    setTimeout(() => {
                        tooltip.style.display = 'none';
                    }, 9000);
                }
            },

            // Theme toggle icon feedback
            setupThemeToggleIcon: function() {
                const themeToggle = document.getElementById('theme-toggle');
                const themeIcon = document.getElementById('theme-icon');
                if (themeToggle && themeIcon) {
                    themeToggle.addEventListener('click', () => {
                        const html = document.documentElement;
                        const isDark = html.getAttribute('data-bs-theme') === 'dark';
                        themeIcon.classList.toggle('fa-moon', !isDark);
                        themeIcon.classList.toggle('fa-sun', isDark);
                    });
                }
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

    // Advanced AI + Speech events
    this.setupAdvancedFeatureEvents();
};

DashboardModule.setupAdvancedFeatureEvents = function() {
    document.getElementById('voiceStartBtn')?.addEventListener('click', () => {
        this.startSpeechCapture('voiceTranscript', 'voiceStatusText');
    });

    document.getElementById('voiceStopBtn')?.addEventListener('click', () => {
        this.stopSpeechCapture('voiceStatusText');
    });

    document.getElementById('voiceUseBtn')?.addEventListener('click', () => {
        this.extractProfileFromSpeech();
    });

    document.getElementById('interviewVoiceBtn')?.addEventListener('click', () => {
        this.startSpeechCapture('interviewAnswer', null, { oneShot: true });
    });

    document.getElementById('generateQuestionBtn')?.addEventListener('click', () => {
        this.generateInterviewQuestion();
    });

    document.getElementById('evaluateInterviewBtn')?.addEventListener('click', () => {
        this.evaluateInterviewAnswer();
    });
};

DashboardModule.startSpeechCapture = function(targetFieldId, statusFieldId, options = {}) {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    const targetEl = document.getElementById(targetFieldId);
    const statusEl = statusFieldId ? document.getElementById(statusFieldId) : null;
    const startBtn = document.getElementById('voiceStartBtn');
    const stopBtn = document.getElementById('voiceStopBtn');

    if (!SpeechRecognition) {
        this.showAlert('warning', 'Speech recognition is not supported in this browser. Please use Chrome or Edge.');
        return;
    }
    if (!targetEl) return;

    if (this._speechRecognition && this._speechActive) {
        this._speechRecognition.stop();
    }

    const recognition = new SpeechRecognition();
    recognition.lang = 'en-US';
    recognition.interimResults = true;
    recognition.continuous = !options.oneShot;

    let finalText = targetEl.value || '';

    recognition.onstart = () => {
        this._speechActive = true;
        this._speechRecognition = recognition;
        if (statusEl) statusEl.textContent = 'Listening...';
        if (startBtn) startBtn.disabled = true;
        if (stopBtn) stopBtn.disabled = false;
    };

    recognition.onresult = (event) => {
        let interim = '';
        for (let i = event.resultIndex; i < event.results.length; i += 1) {
            const transcript = event.results[i][0].transcript;
            if (event.results[i].isFinal) {
                finalText = `${finalText} ${transcript}`.trim();
            } else {
                interim += transcript;
            }
        }
        targetEl.value = `${finalText} ${interim}`.trim();
    };

    recognition.onerror = (event) => {
        this._speechActive = false;
        if (statusEl) statusEl.textContent = `Speech error: ${event.error}`;
        if (startBtn) startBtn.disabled = false;
        if (stopBtn) stopBtn.disabled = true;
    };

    recognition.onend = () => {
        this._speechActive = false;
        if (statusEl) statusEl.textContent = 'Ready';
        if (startBtn) startBtn.disabled = false;
        if (stopBtn) stopBtn.disabled = true;
    };

    recognition.start();
};

DashboardModule.stopSpeechCapture = function(statusFieldId) {
    if (this._speechRecognition && this._speechActive) {
        this._speechRecognition.stop();
    }
    const statusEl = statusFieldId ? document.getElementById(statusFieldId) : null;
    if (statusEl) statusEl.textContent = 'Ready';
};

DashboardModule.extractProfileFromSpeech = function() {
    const transcript = (document.getElementById('voiceTranscript')?.value || '').trim();
    const resultEl = document.getElementById('voiceExtractionResult');

    if (!transcript || transcript.length < 8) {
        this.showAlert('warning', 'Please provide a longer speech transcript first.');
        return;
    }

    const csrfToken = this.getCsrfToken();
    fetch(this.config.apiEndpoints.speechProfileExtract, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-Requested-With': 'XMLHttpRequest',
            ...(csrfToken ? { 'X-CSRFToken': csrfToken } : {})
        },
        body: JSON.stringify({ transcript })
    })
        .then(response => response.json())
        .then(data => {
            if (!data.success || !data.structured_profile) {
                throw new Error(data.message || 'Could not extract profile from speech.');
            }

            const profile = data.structured_profile;
            this.populateManualProfileForm(profile);
            const effective = this.mergeProfiles(profile, this.buildProfileFromCurrentForm());
            this.state.lastProfile = effective;
            this.state.lastSkills = effective.skills || [];
            this.state.hasSessionInput = true;

            const conf = Number(data.confidence || 0);
            if (resultEl) {
                resultEl.innerHTML = `<strong>Profile extracted (${conf}% confidence):</strong> ${
                    (profile.skills || []).length
                } skills, ${(profile.interests || []).length} interests.`;
            }

            this.showAlert('success', 'Speech profile extracted. Manual form auto-filled.');
        })
        .catch(error => {
            if (resultEl) resultEl.textContent = error.message || 'Speech extraction failed.';
            this.showAlert('error', error.message || 'Speech extraction failed.');
        });
};

DashboardModule.generateInterviewQuestion = function() {
    const role = (document.getElementById('interviewRole')?.value || '').trim();
    if (!role) {
        this.showAlert('warning', 'Please enter a target role first.');
        return;
    }

    const csrfToken = this.getCsrfToken();
    fetch(this.config.apiEndpoints.aiInterviewQuestion, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-Requested-With': 'XMLHttpRequest',
            ...(csrfToken ? { 'X-CSRFToken': csrfToken } : {})
        },
        body: JSON.stringify({ role })
    })
        .then(response => response.json())
        .then(data => {
            if (!data.success || !data.question) {
                throw new Error(data.message || 'Could not generate question.');
            }
            const qEl = document.getElementById('interviewQuestion');
            if (qEl) qEl.value = data.question;
            this.showAlert('info', 'Interview question generated.');
        })
        .catch(error => this.showAlert('error', error.message || 'Question generation failed.'));
};

DashboardModule.evaluateInterviewAnswer = function() {
    const role = (document.getElementById('interviewRole')?.value || '').trim();
    const answer = (document.getElementById('interviewAnswer')?.value || '').trim();
    const resultEl = document.getElementById('interviewResult');

    if (!role) {
        this.showAlert('warning', 'Enter target role first.');
        return;
    }
    if (!answer) {
        this.showAlert('warning', 'Please provide an interview answer.');
        return;
    }

    const csrfToken = this.getCsrfToken();
    fetch(this.config.apiEndpoints.aiInterviewEvaluate, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-Requested-With': 'XMLHttpRequest',
            ...(csrfToken ? { 'X-CSRFToken': csrfToken } : {})
        },
        body: JSON.stringify({
            role,
            answer,
            missing_skills: Array.isArray(this.state.lastSkillGap) ? this.state.lastSkillGap : []
        })
    })
        .then(response => response.json())
        .then(data => {
            if (!data.success) {
                throw new Error(data.message || 'Interview evaluation failed.');
            }

            const rubric = data.rubric || {};
            const strengths = (data.strengths || []).map(item => `<li>${item}</li>`).join('');
            const improvements = (data.improvements || []).map(item => `<li>${item}</li>`).join('');
            const nextPlan = (data.personalized_learning_plan || []).map(item => `<li>${item}</li>`).join('');

            if (resultEl) {
                resultEl.innerHTML = `
                    <div><strong>Overall score:</strong> ${data.overall_score}%</div>
                    <div class="rubric-grid">
                        <span class="rubric-chip">Keyword: ${rubric.keyword_coverage || 0}%</span>
                        <span class="rubric-chip">Structure: ${rubric.structure || 0}%</span>
                        <span class="rubric-chip">Impact: ${rubric.impact || 0}%</span>
                        <span class="rubric-chip">Communication: ${rubric.communication || 0}%</span>
                    </div>
                    <div class="mt-2"><strong>Strengths</strong><ul>${strengths || '<li>No major strengths detected yet.</li>'}</ul></div>
                    <div class="mt-2"><strong>Improve next</strong><ul>${improvements || '<li>Keep practicing with more measurable examples.</li>'}</ul></div>
                    <div class="mt-2"><strong>Personalized next-step plan</strong><ul>${nextPlan || '<li>Generate recommendations first to build a targeted learning plan.</li>'}</ul></div>
                `;
            }

            this.showAlert('success', 'Interview answer evaluated successfully.');
        })
        .catch(error => {
            if (resultEl) resultEl.textContent = error.message || 'Interview evaluation failed.';
            this.showAlert('error', error.message || 'Interview evaluation failed.');
        });
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

    // AI + Speech navigation
    document.getElementById('aiUpgradesNav')?.addEventListener('click', (e) => {
        e.preventDefault();
        this.scrollToSection('ai-upgrades');
    });
    
    // Careers navigation
    document.getElementById('careersNav')?.addEventListener('click', (e) => {
        e.preventDefault();
        this.explorecareers();
    });

    // Research metrics navigation
    document.getElementById('researchNav')?.addEventListener('click', (e) => {
        e.preventDefault();
        this.scrollToSection('research-metrics');
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

    // Live jobs empty-state CTA
    document.getElementById('liveJobsCtaBtn')?.addEventListener('click', () => {
        const formProfile = this.buildProfileFromCurrentForm();
        const effectiveProfile = this.mergeProfiles(this.state.lastProfile || {}, formProfile);
        const effectiveSkills = effectiveProfile.skills || [];

        if (!effectiveSkills.length) {
            this.showAlert('warning', 'Add skills first, then run Generate Career Matches.');
            this.scrollToSection('manual-profile');
            return;
        }

        this.loadLiveJobs(this.state.allRecommendationsRaw || this.state.allRecommendations || [], effectiveProfile, effectiveSkills);
    });
    
    // Re-run Analysis button
    document.getElementById('rerunAnalysisBtn')?.addEventListener('click', () => {
        if (this.state.lastProfile) {
            this.submitProfileForAnalysis(this.state.lastProfile, this.state.lastSkills);
        }
    });

    // Clear saved profile button
    document.getElementById('clearProfileBtn')?.addEventListener('click', () => {
        this.clearSavedProfile();
    });
};

DashboardModule.setupFilterEvents = function() {
    const filterInputs = ['filterExperience', 'filterWorkType', 'filterIndustry', 'filterMatchScore', 'filterLocation', 'filterSalary'];
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
                if (inputId === 'filterMatchScore' || inputId === 'filterSalary') {
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
    const rawExperience = (document.getElementById('filterExperience')?.value || '').toString().trim().toLowerCase();
    const rawWorkType = (document.getElementById('filterWorkType')?.value || '').toString().trim().toLowerCase();
    const rawIndustry = (document.getElementById('filterIndustry')?.value || '').toString().trim().toLowerCase();

    this.state.currentFilters = {
        experience: rawExperience === 'all' ? '' : rawExperience,
        workType: rawWorkType === 'all' ? '' : rawWorkType,
        industry: rawIndustry === 'all' ? '' : rawIndustry,
        matchScore: parseInt(document.getElementById('filterMatchScore')?.value || 0),
        location: document.getElementById('filterLocation')?.value?.toLowerCase() || '',
        salaryMin: parseInt(document.getElementById('filterSalary')?.value || 0)
    };
    
    // Filter recommendations
    const baseRecommendations = (this.state.allRecommendationsRaw && this.state.allRecommendationsRaw.length)
        ? this.state.allRecommendationsRaw
        : (this.state.allRecommendations || []);
    let filtered = baseRecommendations;
    
    if (this.state.currentFilters.experience) {
        filtered = filtered.filter(rec => {
            return (rec.experience_level || '').toLowerCase() === this.state.currentFilters.experience.toLowerCase();
        });
    }

    if (this.state.currentFilters.workType) {
        filtered = filtered.filter(rec => {
            const recType = this.normalizeWorkType(rec.work_type || rec.employment_type || rec.description || '');
            return recType === this.state.currentFilters.workType;
        });
    }

    if (this.state.currentFilters.industry) {
        filtered = filtered.filter(rec => {
            const recIndustry = this.normalizeIndustry(rec.industry || rec.job_title || rec.description || '');
            return recIndustry === this.state.currentFilters.industry;
        });
    }

    if (this.state.currentFilters.location) {
        filtered = filtered.filter(rec => {
            const locationText = String(rec.location || '').toLowerCase();
            return locationText.includes(this.state.currentFilters.location);
        });
    }

    if ((this.state.currentFilters.salaryMin || 0) > 0) {
        filtered = filtered.filter(rec => {
            const salaryValue = this.jobSalaryValue(rec);
            return salaryValue && salaryValue >= this.state.currentFilters.salaryMin;
        });
    }
    
    if (this.state.currentFilters.matchScore > 0) {
        filtered = filtered.filter(rec => {
            const score = typeof rec.match_score === 'number' ? (rec.match_score <= 1 ? rec.match_score * 100 : rec.match_score) : 0;
            return score >= this.state.currentFilters.matchScore;
        });
    }
    
    // Re-render with filtered results
    this.renderRecommendations(filtered, this.state.lastSkills || [], { persist: false, filtered: true });

    const totalLiveJobs = (this.state.allLiveJobs || []).length;
    const liveSource = this.state.liveJobsSource || 'adzuna';
    const filteredLiveJobs = this.filterLiveJobs(this.state.allLiveJobs || [], this.state.currentFilters);
    this.renderLiveJobs(filteredLiveJobs, liveSource, { persist: false, filtered: totalLiveJobs > 0 });
    this.updateFilterResultCount(filtered.length, baseRecommendations.length, filteredLiveJobs.length, totalLiveJobs, liveSource);
    
    // Show filter indicator
    const hasActiveFilters = Object.values(this.state.currentFilters).some(v => v !== '' && v !== 0);
    const filterIndicator = document.querySelector('[id="filterPanel"]');
    if (hasActiveFilters && filterIndicator) {
        filterIndicator.style.borderLeft = '3px solid #007bff';
    } else if (filterIndicator) {
        filterIndicator.style.borderLeft = 'none';
    }
};

DashboardModule.updateFilterResultCount = function(filteredMatches, totalMatches, filteredJobs, totalJobs, liveSource = 'adzuna') {
    const counterEl = document.getElementById('filterResultCount');
    if (!counterEl) return;

    const safeFilteredMatches = Number.isFinite(filteredMatches) ? filteredMatches : 0;
    const safeTotalMatches = Number.isFinite(totalMatches) ? totalMatches : 0;
    const safeFilteredJobs = Number.isFinite(filteredJobs) ? filteredJobs : 0;
    const safeTotalJobs = Number.isFinite(totalJobs) ? totalJobs : 0;

    if (safeTotalJobs === 0 && String(liveSource || '').toLowerCase() !== 'adzuna') {
        counterEl.textContent = `Matches: ${safeFilteredMatches}/${safeTotalMatches} | Live jobs: unavailable`;
        return;
    }

    counterEl.textContent = `Matches: ${safeFilteredMatches}/${safeTotalMatches} | Live jobs: ${safeFilteredJobs}/${safeTotalJobs}`;
};

DashboardModule.normalizeExperienceLevel = function(value) {
    const text = String(value || '').toLowerCase();
    if (!text) return '';
    if (/(senior|lead|principal|staff|architect|expert)/.test(text)) return 'senior';
    if (/(mid|intermediate)/.test(text)) return 'mid';
    if (/(entry|junior|fresher|graduate|intern)/.test(text)) return 'entry';
    return '';
};

DashboardModule.normalizeWorkType = function(value) {
    const text = String(value || '').toLowerCase();
    if (!text) return '';
    if (text.includes('hybrid')) return 'hybrid';
    if (text.includes('remote') || text.includes('work from home') || text.includes('wfh')) return 'remote';
    return 'onsite';
};

DashboardModule.normalizeIndustry = function(value) {
    const text = String(value || '').toLowerCase();
    if (!text) return '';
    if (/fintech|bank|payments/.test(text)) return 'fintech';
    if (/health|healthcare|medical|hospital/.test(text)) return 'healthcare';
    if (/ecommerce|e-commerce|retail/.test(text)) return 'ecommerce';
    if (/consulting|consultant|advisory/.test(text)) return 'consulting';
    return 'technology';
};

DashboardModule.inferJobExperienceLevel = function(job) {
    const direct = this.normalizeExperienceLevel(job.experience_level);
    if (direct) return direct;

    const text = `${job.job_title || ''} ${job.description || ''}`.toLowerCase();
    if (!text) return '';

    if (/(senior|lead|principal|staff|architect|\b[6-9]\+\s*years|\b10\+\s*years)/.test(text)) return 'senior';
    if (/(mid|intermediate|\b[3-5]\+\s*years)/.test(text)) return 'mid';
    if (/(entry|junior|fresher|graduate|intern|\b0-2\s*years|\b[1-2]\+\s*years)/.test(text)) return 'entry';

    return '';
};

DashboardModule.jobSalaryValue = function(job) {
    const min = Number(job.salary_min || 0);
    const max = Number(job.salary_max || 0);
    if (min > 0 && max > 0) return Math.round((min + max) / 2);
    return min || max || 0;
};

DashboardModule.filterLiveJobs = function(jobs, filters) {
    if (!Array.isArray(jobs) || !jobs.length) return [];

    return jobs.filter(job => {
        if (filters.location) {
            const locationText = String(job.location || '').toLowerCase();
            if (!locationText.includes(filters.location)) return false;
        }

        if (filters.experience) {
            const level = this.inferJobExperienceLevel(job);
            if (level !== filters.experience) return false;
        }

        if (filters.workType) {
            const workType = this.normalizeWorkType(job.employment_type || job.description || job.location || '');
            if (workType !== filters.workType) return false;
        }

        if (filters.industry) {
            const industry = this.normalizeIndustry(job.industry || job.job_title || job.description || '');
            if (industry !== filters.industry) return false;
        }

        if ((filters.salaryMin || 0) > 0) {
            const salaryValue = this.jobSalaryValue(job);
            if (!salaryValue || salaryValue < filters.salaryMin) return false;
        }

        return true;
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
    // Clear previous analysis output before processing a new resume file.
    this.resetAnalysisOutputs();
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
            this.handleUploadError(error.message || 'Upload failed. Please try again.');
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

        const contentType = response.headers.get('content-type') || '';
        const isJson = contentType.includes('application/json');
        const payload = isJson ? await response.json() : null;

        if (!response.ok) {
            const message = payload && (payload.error || payload.message)
                ? (payload.error || payload.message)
                : `Upload failed (${response.status}).`;
            throw new Error(message);
        }

        return payload || {};
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

    // For upload mode, analyze resume-extracted skills only (avoid stale manual profile reuse).
    const resumeOnlyProfile = this.mergeProfiles(profilePayload, {});
    const resumeOnlySkills = resumeOnlyProfile.skills || [];
    this.updateExtractedSkillsPanel(resumeOnlySkills);

    this.setProfileStatus('Resume parsed');
    // Update form fields only with extracted values; preserve existing manual values when extracted is blank.
    this.populateManualProfileForm(profilePayload);

    if (!resumeOnlySkills.length) {
        this.state.lastProfile = null;
        this.state.lastSkills = [];
        this.setProfileStatus('Resume parsed. Add skills to run matching.');
        this.resetAnalysisOutputs();
        this.showAlert('warning', 'Resume upload succeeded, but no reliable skills were extracted from this file. Add skills manually or upload a clearer resume format.');
        return;
    }

    this.state.lastProfile = resumeOnlyProfile;
    this.state.lastSkills = resumeOnlySkills;
    this.state.hasSessionInput = true;
    this.showAlert('info', `Using ${resumeOnlySkills.length} resume-extracted skills for matching: ${resumeOnlySkills.slice(0, 8).join(', ')}${resumeOnlySkills.length > 8 ? '...' : ''}`);

    this.submitProfileForAnalysis(resumeOnlyProfile, resumeOnlySkills);
};

DashboardModule.resetAnalysisOutputs = function() {
    this.showEmptyRecommendations();
    this.updateSkillGapSummary([]);
    this.updateRoadmap([]);
    this.resetLiveJobsPanel({
        marketTitle: 'Live Market Snapshot',
        marketSubtitle: 'Live job opportunities powered by Adzuna API.',
        title: 'Live Jobs Not Loaded',
        subtitle: 'Complete your profile and run matching to load relevant live jobs.'
    });

    this.state.allRecommendations = [];
    this.state.allRecommendationsRaw = [];
    this.state.allLiveJobs = [];
    this.state.liveJobsSource = 'adzuna';
    this.state.lastSkillGap = [];
    this.resetResearchMetrics();

    const filterPanel = document.getElementById('filterPanel');
    if (filterPanel) filterPanel.classList.add('d-none');

    const rerunBtn = document.getElementById('rerunAnalysisBtn');
    if (rerunBtn) rerunBtn.style.display = 'none';
};

DashboardModule.resetResearchMetrics = function() {
    const cards = document.querySelectorAll('#researchMetricsCards .research-metric-value');
    cards.forEach(node => {
        node.textContent = '--';
    });

    const breakdown = document.getElementById('researchFairnessBreakdown');
    if (breakdown) {
        breakdown.textContent = 'Generate recommendations to see fairness and calibration breakdown.';
    }
};

DashboardModule.updateResearchMetrics = function(recommendations) {
    if (!Array.isArray(recommendations) || !recommendations.length) {
        this.resetResearchMetrics();
        return;
    }

    const coverageValues = [];
    const confidenceValues = [];
    const calibrationGaps = [];

    const experienceBuckets = { entry: 0, mid: 0, senior: 0, unknown: 0 };
    const industryBuckets = {};

    recommendations.forEach(rec => {
        const required = this.parseRequiredSkills(rec.required_skills);
        const matched = Array.isArray(rec.matched_skills) ? rec.matched_skills : [];
        const requiredCount = Math.max(1, required.length);
        const overlap = matched.length / requiredCount;
        coverageValues.push(overlap * 100);

        const confidence = Number(rec.confidence);
        const normalizedConfidence = Number.isFinite(confidence)
            ? Math.max(0, Math.min(100, confidence))
            : (overlap * 100);

        confidenceValues.push(normalizedConfidence);
        calibrationGaps.push(Math.abs(normalizedConfidence - overlap * 100));

        const level = this.normalizeExperienceLevel(rec.experience_level || '');
        if (!level) {
            experienceBuckets.unknown += 1;
        } else {
            experienceBuckets[level] += 1;
        }

        const industry = this.normalizeIndustry(rec.industry || rec.job_title || rec.description || '') || 'technology';
        industryBuckets[industry] = (industryBuckets[industry] || 0) + 1;
    });

    const avgCoverage = coverageValues.reduce((a, b) => a + b, 0) / coverageValues.length;
    const avgConfidence = confidenceValues.reduce((a, b) => a + b, 0) / confidenceValues.length;
    const meanCalibrationGap = calibrationGaps.reduce((a, b) => a + b, 0) / calibrationGaps.length;

    const experienceShares = ['entry', 'mid', 'senior'].map(key => (experienceBuckets[key] / recommendations.length) * 100);
    const fairnessSpread = Math.max(...experienceShares) - Math.min(...experienceShares);

    const metricValues = document.querySelectorAll('#researchMetricsCards .research-metric-value');
    if (metricValues[0]) metricValues[0].textContent = `${Math.round(avgCoverage)}%`;
    if (metricValues[1]) metricValues[1].textContent = `${Math.round(meanCalibrationGap)}%`;
    if (metricValues[2]) metricValues[2].textContent = `${Math.round(avgConfidence)}%`;
    if (metricValues[3]) metricValues[3].textContent = `${Math.round(fairnessSpread)}%`;

    const topIndustries = Object.entries(industryBuckets)
        .sort((a, b) => b[1] - a[1])
        .slice(0, 3)
        .map(([name, count]) => `${name} (${count})`)
        .join(', ');

    const breakdown = document.getElementById('researchFairnessBreakdown');
    if (breakdown) {
        breakdown.innerHTML = `
            <strong>Fairness breakdown:</strong>
            <ul>
                <li>Experience exposure: Entry ${Math.round(experienceShares[0])}%, Mid ${Math.round(experienceShares[1])}%, Senior ${Math.round(experienceShares[2])}%.</li>
                <li>Top industry exposure: ${topIndustries || 'No dominant industry.'}.</li>
                <li>Calibration proxy: Lower gap indicates better confidence alignment with observed overlap.</li>
            </ul>
        `;
    }
};

DashboardModule.updateExtractedSkillsPanel = function(skills) {
    const panel = document.getElementById('extractedSkillsPanel');
    const list = document.getElementById('extractedSkillsList');
    if (!panel || !list) return;

    if (!Array.isArray(skills) || !skills.length) {
        panel.classList.add('d-none');
        list.innerHTML = '';
        return;
    }

    list.innerHTML = skills.slice(0, 16)
        .map(skill => `<span class="tag-item matching" style="margin-right: 6px; margin-bottom: 6px; display: inline-block;">${skill}</span>`)
        .join('');
    panel.classList.remove('d-none');
};

DashboardModule.clearSavedProfile = function() {
    const csrfToken = this.getCsrfToken();

    fetch(this.config.apiEndpoints.clearProfile, {
        method: 'DELETE',
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
            ...(csrfToken ? { 'X-CSRFToken': csrfToken } : {})
        }
    })
        .then(async response => {
            const payload = await response.json().catch(() => ({}));
            if (!response.ok) {
                throw new Error(payload.error || 'Failed to clear saved profile.');
            }
            return payload;
        })
        .then(() => {
            this.state.lastProfile = null;
            this.state.lastSkills = [];
            this.state.allRecommendations = [];
            this.state.allRecommendationsRaw = [];
            this.state.hasSessionInput = false;
            this.setProfileStatus('Saved profile cleared.');
            this.updateProfileCompletion({});
            this.updateExtractedSkillsPanel([]);

            const form = document.getElementById('manualProfileForm');
            form?.reset();

            this.resetAnalysisOutputs();
            this.showAlert('success', 'Saved profile cleared. You can start fresh.');
        })
        .catch(error => {
            this.showAlert('error', error.message || 'Could not clear saved profile.');
        });
};

DashboardModule.hasMeaningfulProfile = function(profile) {
    if (!profile || typeof profile !== 'object') return false;
    const skills = Array.isArray(profile.skills) ? profile.skills : [];
    const interests = Array.isArray(profile.interests) ? profile.interests : [];
    const degrees = profile.education && Array.isArray(profile.education.degrees)
        ? profile.education.degrees
        : [];
    const exp = Array.isArray(profile.experience) ? profile.experience : [];
    return skills.length > 0 || interests.length > 0 || degrees.length > 0 || exp.length > 0;
};

DashboardModule.mergeProfiles = function(primary, fallback) {
    const p = primary && typeof primary === 'object' ? primary : {};
    const f = fallback && typeof fallback === 'object' ? fallback : {};

    const mergedSkills = Array.from(new Set([...(p.skills || []), ...(f.skills || [])]));
    const mergedInterests = Array.from(new Set([...(p.interests || []), ...(f.interests || [])]));
    const pDegrees = p.education && Array.isArray(p.education.degrees) ? p.education.degrees : [];
    const fDegrees = f.education && Array.isArray(f.education.degrees) ? f.education.degrees : [];
    const mergedDegrees = Array.from(new Set([...pDegrees, ...fDegrees])).filter(Boolean);

    const pYears = Array.isArray(p.experience) && p.experience.length ? Number(p.experience[0].years || 0) : 0;
    const fYears = Array.isArray(f.experience) && f.experience.length ? Number(f.experience[0].years || 0) : 0;
    const mergedYears = Math.max(pYears, fYears, 0);

    return {
        skills: mergedSkills,
        interests: mergedInterests,
        education: { degrees: mergedDegrees },
        experience: mergedYears > 0 ? [{ years: mergedYears }] : []
    };
};

DashboardModule.buildProfileFromCurrentForm = function() {
    const educationLevel = document.getElementById('educationLevel')?.value.trim() || '';
    const yearsExperienceRaw = document.getElementById('yearsExperience')?.value;
    const skillsInput = document.getElementById('skillsInput')?.value || '';
    const interestArea = document.getElementById('interestArea')?.value || '';

    const skills = this.normalizeSkills(skillsInput);
    const interests = this.normalizeSkills(interestArea);
    const yearsExperience = yearsExperienceRaw ? parseFloat(yearsExperienceRaw) : 0;

    return {
        skills,
        interests,
        education: { degrees: educationLevel ? [educationLevel] : [] },
        experience: yearsExperience ? [{ years: yearsExperience }] : []
    };
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
    this.state.hasSessionInput = true;
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
        .then(async response => {
            const contentType = response.headers.get('content-type') || '';
            const isJson = contentType.includes('application/json');
            const payload = isJson ? await response.json() : null;

            if (!response.ok) {
                const message = payload && (payload.error || payload.message)
                    ? (payload.error || payload.message)
                    : `Profile analysis failed (${response.status}).`;
                throw new Error(message);
            }

            if (!payload) {
                throw new Error('Unexpected server response while analyzing profile.');
            }

            return payload;
        })
        .then(data => {
            // Profile analysis completed

            if (data.data_message) {
                if (data.data_source && data.data_source !== 'adzuna') {
                    this.setProfileStatus('Live market data unavailable');
                    this.showAlert('warning', data.data_message);
                } else {
                    this.showAlert('info', data.data_message);
                }
            }

            if (data.recommendations && data.recommendations.length) {
                this.renderRecommendations(data.recommendations, userSkills);
                this.updateResearchMetrics(data.recommendations);
                this.setProfileStatus('Recommendations ready');
            } else {
                if (!data.data_message) {
                    this.showAlert('warning', 'No skill-based career matches found yet. Add or refine skills and try again.');
                }
                this.showEmptyRecommendations();
                this.updateSkillGapSummary([]);
                this.updateRoadmap([]);
                this.resetLiveJobsPanel({
                    marketTitle: 'Live Market Snapshot',
                    marketSubtitle: 'Live job opportunities powered by Adzuna API.',
                    title: 'No Relevant Live Jobs Yet',
                    subtitle: 'Run matching with more skills to load relevant live jobs.'
                });
                this.resetResearchMetrics();
                return;
            }

            const roleGap = Array.isArray(data.skill_gap) ? data.skill_gap : [];
            const roleRoadmap = Array.isArray(data.roadmap) ? data.roadmap : [];
            this.state.lastSkillGap = roleGap;

            this.updateSkillGapSummary(roleGap);
            this.updateRoadmap(roleRoadmap);

            // Prefer live jobs returned from the same analysis call for consistency.
            if (Array.isArray(data.live_jobs) && data.live_jobs.length) {
                this.renderLiveJobs(data.live_jobs, data.data_source || 'adzuna');
                this.applyFilters();
            } else {
                if (data.data_source && data.data_source !== 'adzuna') {
                    this.resetLiveJobsPanel({
                        marketTitle: 'Live Market Snapshot',
                        marketSubtitle: 'Live job data unavailable. Please refresh or try again later.',
                        title: 'Live Jobs Unavailable',
                        subtitle: 'Live API jobs are temporarily unavailable. Career recommendations are generated from local role catalog data.'
                    });
                    this.applyFilters();
                    return;
                }
                // Fallback fetch using matched careers context.
                this.loadLiveJobs(data.recommendations, profilePayload, userSkills);
            }
        })
        .catch(error => {
            console.error('Profile analysis error:', error);
            this.showAlert('error', error.message || 'Profile analysis failed. Please try again.');
        })
        .finally(() => {
            this.hideLoadingOverlay();
        });
};

DashboardModule.buildLiveQuery = function(recommendations, profilePayload, userSkills) {
    const topRoles = Array.isArray(recommendations)
        ? recommendations
            .filter(rec => typeof rec.match_score === 'number' && rec.match_score > 0)
            .slice(0, 3)
            .map(rec => rec.job_title)
            .filter(Boolean)
        : [];

    if (topRoles.length) {
        return topRoles.join(' OR ');
    }

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

    return '';
};

DashboardModule.resetLiveJobsPanel = function(options = {}) {
    const list = document.getElementById('liveJobsList');
    const empty = document.getElementById('liveJobsEmpty');
    const title = document.getElementById('liveMarketTitle');
    const subtitle = document.getElementById('liveMarketSubtitle');
    if (!list || !empty) return;

    if (title && options.marketTitle) title.textContent = options.marketTitle;
    if (subtitle && options.marketSubtitle) subtitle.textContent = options.marketSubtitle;

    const emptyTitle = empty.querySelector('h6');
    const emptyText = empty.querySelector('p');
    if (emptyTitle && options.title) emptyTitle.textContent = options.title;
    if (emptyText && options.subtitle) emptyText.textContent = options.subtitle;

    list.classList.add('d-none');
    empty.classList.remove('d-none');
};

DashboardModule.renderLiveJobs = function(jobs, source = 'adzuna', options = {}) {
    const list = document.getElementById('liveJobsList');
    const empty = document.getElementById('liveJobsEmpty');
    const title = document.getElementById('liveMarketTitle');
    const subtitle = document.getElementById('liveMarketSubtitle');
    if (!list || !empty) return;

    if (options.persist !== false) {
        this.state.allLiveJobs = Array.isArray(jobs) ? jobs.slice() : [];
        this.state.liveJobsSource = source;
    }

    const sourceValue = String(source || '').toLowerCase();
    if (title) {
        title.textContent = sourceValue === 'adzuna' ? 'Live Market Snapshot — India' : 'Live Market Snapshot';
    }
    if (subtitle) {
        subtitle.textContent = sourceValue === 'adzuna'
            ? 'Real-time job opportunities powered by Adzuna API.'
            : 'Live job data unavailable. Please refresh or try again later.';
    }

    if (!Array.isArray(jobs) || !jobs.length) {
        const sourceUnavailable = sourceValue !== 'adzuna';
        const isFilteredView = options.filtered === true && !sourceUnavailable;

        this.resetLiveJobsPanel({
            marketTitle: 'Live Market Snapshot',
            marketSubtitle: sourceUnavailable
                ? 'Live job data unavailable. Please refresh or try again later.'
                : 'Real-time job opportunities powered by Adzuna API.',
            title: isFilteredView ? 'No Jobs Match Current Filters' : 'Live Jobs Unavailable',
            subtitle: isFilteredView
                ? 'Try broader location, experience, or salary filters.'
                : 'Live job data unavailable. Please refresh or try again later.'
        });
        return;
    }

    const cards = jobs.slice(0, 6).map(job => {
        const experienceLevel = this.inferJobExperienceLevel(job);
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
                    <div><i class="fas fa-user-clock me-1"></i>${experienceLevel ? (experienceLevel.charAt(0).toUpperCase() + experienceLevel.slice(1)) : 'Experience not specified'}</div>
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
    this.updateDataSourceTimestamp();
};

DashboardModule.loadLiveJobs = function(recommendations, profilePayload, userSkills) {
    const list = document.getElementById('liveJobsList');
    const empty = document.getElementById('liveJobsEmpty');
    const title = document.getElementById('liveMarketTitle');
    const subtitle = document.getElementById('liveMarketSubtitle');
    if (!list || !empty) return;

    const query = this.buildLiveQuery(recommendations, profilePayload, userSkills);
    if (!query) {
        this.resetLiveJobsPanel({
            marketTitle: 'Live Market Snapshot',
            marketSubtitle: 'Live job opportunities powered by Adzuna API.',
            title: 'Live Jobs Not Loaded',
            subtitle: 'Complete your profile and run matching to load relevant live jobs.'
        });
        return;
    }

    const params = new URLSearchParams({ query: query, location: 'India', results: 20 });

    fetch(`${this.config.apiEndpoints.liveJobs}?${params.toString()}`)
        .then(response => response.json())
        .then(data => {
            const source = (data && data.source) ? String(data.source).toLowerCase() : '';
            if (title) {
                title.textContent = source === 'adzuna'
                    ? 'Live Market Snapshot — India'
                    : 'Live Market Snapshot';
            }
            if (subtitle) {
                subtitle.textContent = source === 'adzuna'
                    ? 'Real-time job opportunities powered by Adzuna API'
                    : 'Live job data unavailable. Please refresh or try again later.';
            }

            const jobs = (data && data.live_jobs && data.live_jobs.length)
                ? data.live_jobs
                : (data && data.jobs && data.jobs.length ? data.jobs : []);

            this.renderLiveJobs(jobs, source);
            this.applyFilters();
        })
        .catch(() => {
            this.resetLiveJobsPanel({
                title: 'Live Jobs Unavailable',
                subtitle: 'Live job data unavailable. Please refresh or try again later.'
            });
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

DashboardModule.renderRecommendations = function(recommendations, userSkills, options = {}) {
    const list = document.getElementById('recommendationsList');
    const empty = document.getElementById('recommendationsEmpty');
    const isFilteredView = options.filtered === true;
    const shouldPersist = options.persist !== false;

    if (!list || !empty) return;

    const allSourceRecs = Array.isArray(recommendations) ? recommendations.slice() : [];
    if (!isFilteredView) {
        // Store all source recommendations for filter re-application
        this.state.allRecommendationsRaw = allSourceRecs.slice();
    }

    const skillsLower = userSkills.map(skill => skill.toLowerCase());
    const aggregatedMissing = new Set();

    let allRecs = [];

    if (isFilteredView) {
        allRecs = allSourceRecs.slice(0, 6);
    } else {
        const suitableRecs = allSourceRecs.filter(rec => {
            const score = typeof rec.match_score === 'number'
                ? (rec.match_score <= 1 ? rec.match_score * 100 : rec.match_score)
                : 0;
            const matchedCount = Array.isArray(rec.matched_skills) ? rec.matched_skills.length : 0;
            return score >= 40 && matchedCount >= 2;
        });

        allRecs = suitableRecs.slice(0, 6);

        if (!allRecs.length) {
            const lowConfidence = allSourceRecs.filter(rec => {
                const score = typeof rec.match_score === 'number'
                    ? (rec.match_score <= 1 ? rec.match_score * 100 : rec.match_score)
                    : 0;
                const matchedCount = Array.isArray(rec.matched_skills) ? rec.matched_skills.length : 0;
                return score >= 25 && matchedCount >= 1;
            });

            if (lowConfidence.length) {
                allRecs = lowConfidence.slice(0, 4);
                this.showAlert('info', 'Showing low-confidence matches. Add more skills for stronger recommendations.');
            }
        }
    }

    if (!allRecs.length) {
        list.classList.add('d-none');
        empty.classList.remove('d-none');

        const emptyTitle = empty.querySelector('h6');
        const emptyText = empty.querySelector('p');
        if (emptyTitle) emptyTitle.textContent = isFilteredView ? 'No Matches For Current Filters' : 'No Skill-Based Matches Yet';
        if (emptyText) {
            emptyText.textContent = isFilteredView
                ? 'Try broader filter settings to see more matching roles.'
                : 'No career reached a positive overlap score. Add relevant skills and run analysis again.';
        }

        this.state.allRecommendations = [];

        const filterPanel = document.getElementById('filterPanel');
        if (filterPanel && !isFilteredView) filterPanel.classList.add('d-none');

        const rerunBtn = document.getElementById('rerunAnalysisBtn');
        if (rerunBtn && !isFilteredView) rerunBtn.style.display = 'none';

        return;
    }

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
                        <div class="small text-muted mt-1">
                            Confidence: <strong>${String(rec.confidence_band || 'medium').toUpperCase()}</strong>
                            ${Array.isArray(rec.confidence_range) ? `(${rec.confidence_range[0]}%-${rec.confidence_range[1]}%)` : ''}
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
                                ${rec.counterfactual && rec.counterfactual.message ? `<li>${rec.counterfactual.message}</li>` : ''}
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
                ${rec.counterfactual && Array.isArray(rec.counterfactual.suggested_skills) && rec.counterfactual.suggested_skills.length ? `
                <div style="margin-top: 10px; background: #f4fbff; border: 1px solid #d8ecff; border-radius: 10px; padding: 10px;">
                    <div class="small text-muted">Counterfactual improvement</div>
                    <div class="small">
                        Learn <strong>${rec.counterfactual.suggested_skills.join(', ')}</strong>
                        to target ~<strong>${Math.round(rec.counterfactual.estimated_score || scoreValue)}%</strong>
                        (${Math.round(rec.counterfactual.estimated_gain || 0)}% gain)
                    </div>
                </div>` : ''}
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
    
    // Store full source for future filter operations (including filters and "all" view behavior).
    if (shouldPersist) {
        this.state.allRecommendationsRaw = allSourceRecs.slice();
    }
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

    // Skill gap and roadmap are rendered from role-overlap results in submitProfileForAnalysis.
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
        container.className = 'empty-state compact';
        container.innerHTML = `
            <i class="fas fa-chart-bar"></i>
            <h6>No Skill Gaps Yet</h6>
            <p>Generate recommendations to view role-wise missing skills.</p>
        `;
        return;
    }

    container.className = 'tag-list';
    container.innerHTML = missingSkills
        .slice(0, 8)
        .map(skill => `<span class="tag-item missing">${skill}</span>`)
        .join('');
};

DashboardModule.updateRoadmap = function(roadmapItems) {
    const list = document.getElementById('roadmapList');
    if (!list) return;

    if (!roadmapItems.length) {
        list.innerHTML = '<li>Complete a profile to generate a learning roadmap.</li>';
        return;
    }

    list.innerHTML = roadmapItems.slice(0, 6)
        .map(item => {
            const skill = item.skill || item.phase || 'Skill';
            const actions = Array.isArray(item.actions) ? item.actions.slice(0, 4) : [];
            const actionsHtml = actions.map(step => `<li>${step}</li>`).join('');
            return `
                <li style="margin-bottom: 1rem;">
                    <strong>${skill}</strong>
                    <ol style="margin-top: 0.4rem;">${actionsHtml}</ol>
                </li>
            `;
        })
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
                list.className = 'empty-state compact';
                list.innerHTML = `
                    <i class="fas fa-comments"></i>
                    <h6>No Feedback History Yet</h6>
                    <p>Rate recommendations and your feedback history will appear here.</p>
                `;
                return;
            }
            list.className = '';
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

DashboardModule.updateProfileCompletion = function(profile, mode = 'active') {
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
    const hasEducation = profile && profile.education && (
        (typeof profile.education.degree === 'string' && profile.education.degree.length > 0) ||
        (Array.isArray(profile.education.degrees) && profile.education.degrees.length > 0)
    );
    if (hasEducation) {
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
        if (mode === 'saved') {
            progressBar.classList.remove('bg-success');
            progressBar.classList.add('bg-info');
        } else {
            progressBar.classList.remove('bg-info');
            progressBar.classList.add('bg-success');
        }
    }
    
    if (completionText) {
        completionText.textContent = `${completionPercent}% complete`;
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
    const formProfile = this.buildProfileFromCurrentForm();
    const effectiveProfile = this.mergeProfiles(this.state.lastProfile || {}, formProfile);

    if (!this.hasMeaningfulProfile(effectiveProfile)) {
        this.showAlert('warning', 'Choose a resume or manual profile input first.');
        this.scrollToSection('input-modes');
        return;
    }

    if (!Array.isArray(effectiveProfile.skills) || effectiveProfile.skills.length === 0) {
        this.setProfileStatus('Skills required for matching');
        this.showAlert('warning', 'Add at least one skill in Manual Profile or upload a resume with identifiable skills.');
        this.scrollToSection('manual-profile');
        this.showEmptyRecommendations();
        return;
    }

    this.state.lastProfile = effectiveProfile;
    this.state.lastSkills = effectiveProfile.skills || [];
    this.state.hasSessionInput = true;
    this.submitProfileForAnalysis(effectiveProfile, this.state.lastSkills);
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
    
    // Create alert element with unique id
    const alertId = 'alert-' + Date.now() + '-' + Math.floor(Math.random() * 10000);
    const alertHTML = `
        <div id="${alertId}" class="alert alert-${type === 'error' ? 'danger' : type} alert-dismissible fade show notification-slide-in" role="alert" style="position: fixed; top: 20px; right: 20px; z-index: 9999; min-width: 300px;">
            <i class="fas fa-${this.getAlertIcon(type)} me-2"></i>
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    `;
    document.body.insertAdjacentHTML('beforeend', alertHTML);
    // Auto remove after 5 seconds
    setTimeout(() => {
        const alert = document.getElementById(alertId);
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
    this.state.currentUser = null;
    this.state.hasSessionInput = false;

    fetch(this.config.apiEndpoints.currentProfile, {
        method: 'GET',
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('Could not load saved profile.');
            }
            return response.json();
        })
        .then(data => {
            if (!data || !data.has_profile || !data.profile) {
                return;
            }

            const profile = data.profile;
            const savedSkills = Array.isArray(profile.skills) ? profile.skills : [];
            if (this.hasMeaningfulProfile(profile)) {
                this.state.lastProfile = profile;
                this.state.lastSkills = savedSkills;
                this.state.hasSessionInput = true;
                this.populateManualProfileForm(profile);
                this.updateProfileCompletion(profile, 'saved');
                this.setProfileStatus(savedSkills.length ? `Saved profile loaded (${savedSkills.length} skills)` : 'Saved profile loaded');
                return;
            }

            this.state.lastProfile = null;
            this.state.lastSkills = [];
            this.updateProfileCompletion({});
            this.setProfileStatus('No profile');
            this.resetLiveJobsPanel({
                title: 'Live Jobs Not Loaded',
                subtitle: 'Complete your profile and run matching to load relevant live jobs.'
            });
        })
        .catch(error => {
            console.warn('Profile auto-load skipped:', error);
        });
};

DashboardModule.populateManualProfileForm = function(profile) {
    if (!profile || typeof profile !== 'object') return;

    const educationLevel = profile.education && Array.isArray(profile.education.degrees)
        ? (profile.education.degrees[0] || '')
        : '';

    const yearsExperience = Array.isArray(profile.experience) && profile.experience.length
        ? (profile.experience[0].years || 0)
        : 0;

    const skills = Array.isArray(profile.skills) ? profile.skills.join(', ') : '';
    const interests = Array.isArray(profile.interests) ? profile.interests.join(', ') : '';

    const educationEl = document.getElementById('educationLevel');
    const yearsEl = document.getElementById('yearsExperience');
    const skillsEl = document.getElementById('skillsInput');
    const interestsEl = document.getElementById('interestArea');

    // Preserve existing user-entered values when incoming payload has blanks.
    if (educationEl && educationLevel) educationEl.value = educationLevel;
    if (yearsEl && yearsExperience) yearsEl.value = yearsExperience;
    if (skillsEl && skills) skillsEl.value = skills;
    if (interestsEl && interests) interestsEl.value = interests;
};

window.DashboardModule = DashboardModule;
