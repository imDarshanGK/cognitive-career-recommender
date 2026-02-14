"""
Service module init
"""

from .auth_service import AuthService
from .profile_service import ProfileService
from .resume_service import ResumeService
from .skill_extractor import SkillExtractor
from .job_loader import JobDatasetLoader

# Optional imports that may not be available
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

__all__ = [
    'AuthService',
    'ProfileService', 
    'ResumeService',
    'SkillExtractor',
    'JobDatasetLoader',
    'SkillMatcher',
    'CognitiveReasoner',
    'XAIExplainer',
    'RoadmapGenerator'
]
