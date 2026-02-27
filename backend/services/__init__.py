"""
Service module init for Cognitive Career Recommendation System
Centralizes business logic and AI service orchestration.
"""

from .auth_service import AuthService
from .profile_service import ProfileService
from .resume_service import ResumeService
from .skill_extractor import SkillExtractor
from .job_loader import JobDatasetLoader

# Optional AI components with safe fallbacks
try:
    from .skill_matcher import SkillMatcher
except ImportError:
    SkillMatcher = None

try:
    from .cognitive_reasoner import CognitiveReasoner
except ImportError:
    CognitiveReasoner = None

try:
    from .xai_explainer import XAIExplainer
except ImportError:
    XAIExplainer = None

try:
    from .roadmap_generator import RoadmapGenerator
except ImportError:
    RoadmapGenerator = None

def get_available_services():
    """Returns a list of currently active AI services for system health monitoring."""
    services = {
        'core': ['AuthService', 'ProfileService', 'ResumeService', 'SkillExtractor'],
        'cognitive': []
    }
    if SkillMatcher: services['cognitive'].append('SkillMatcher')
    if CognitiveReasoner: services['cognitive'].append('CognitiveReasoner')
    if XAIExplainer: services['cognitive'].append('XAIExplainer')
    if RoadmapGenerator: services['cognitive'].append('RoadmapGenerator')
    return services

__all__ = [
    'AuthService',
    'ProfileService', 
    'ResumeService',
    'SkillExtractor',
    'JobDatasetLoader',
    'SkillMatcher',
    'CognitiveReasoner',
    'XAIExplainer',
    'RoadmapGenerator',
    'get_available_services'
]