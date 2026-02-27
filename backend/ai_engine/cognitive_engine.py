"""
Cognitive AI Engine for Career & Job Recommendation System
Implements the cognitive loop: Observe → Understand → Analyze → Reason → Decide → Explain → Learn
"""

import numpy as np
import pandas as pd
import os
from typing import Dict, List, Any, Tuple
from datetime import datetime

# Optional imports for Machine Learning and Explainable AI
try:
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False

try:
    from lime.lime_text import LimeTextExplainer
    EXPLAINER_AVAILABLE = True
except ImportError:
    EXPLAINER_AVAILABLE = False

try:
    import joblib
    JOBLIB_AVAILABLE = True
except ImportError:
    JOBLIB_AVAILABLE = False

class CognitiveRecommendationEngine:
    """
    Core cognitive AI engine that simulates human-like thinking for career recommendations
    """
    
    def __init__(self):
        self.job_model = None
        self.skill_vectorizer = None
        self.job_data = None
        self.user_feedback_history = []
        self.reasoning_memory = {}
        
        # Centralized Path Management
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.backend_dir = os.path.dirname(self.current_dir)
        
        self._initialize_models()
        self._load_job_data()

    def _initialize_models(self):
        """Initialize machine learning models and XAI components with fallback logic"""
        models_dir = os.path.join(self.backend_dir, 'models')
        os.makedirs(models_dir, exist_ok=True)
        
        model_path = os.path.join(models_dir, 'job_recommendation_model.pkl')
        vec_path = os.path.join(models_dir, 'skill_vectorizer.pkl')

        if JOBLIB_AVAILABLE:
            try:
                self.job_model = joblib.load(model_path)
                self.skill_vectorizer = joblib.load(vec_path)
            except Exception:
                self.job_model = None
                self.skill_vectorizer = None

        if (self.job_model is None or self.skill_vectorizer is None) and SKLEARN_AVAILABLE:
            self.job_model = RandomForestClassifier(n_estimators=10, random_state=42)
            self.skill_vectorizer = TfidfVectorizer(max_features=100, stop_words='english')
        
        self.lime_explainer = LimeTextExplainer(class_names=['Not Suitable', 'Suitable']) if EXPLAINER_AVAILABLE else None

    def _load_job_data(self):
        """Load job market data with validation"""
        data_path = os.path.join(self.backend_dir, 'data', 'job_dataset.csv')
        
        try:
            if os.path.exists(data_path):
                self.job_data = pd.read_csv(data_path)
                required = ['job_title', 'required_skills', 'experience_level', 'industry']
                if not all(col in self.job_data.columns for col in required):
                    self.job_data = self._create_sample_job_data()
            else:
                self.job_data = self._create_sample_job_data()
        except Exception:
            self.job_data = self._create_sample_job_data()

    def _create_sample_job_data(self):
        """Fallback dataset for testing and initial deployment"""
        jobs = [
            ['Data Scientist', 'Python, ML, Statistics', 'Mid-level', 'Technology', '80000-120000'],
            ['Software Engineer', 'Java, Python, SQL', 'Entry-level', 'Technology', '60000-100000'],
            ['Product Manager', 'Strategy, Analytics', 'Senior-level', 'Technology', '100000-150000'],
            ['UX Designer', 'Design, Research', 'Mid-level', 'Design', '70000-110000'],
            ['Data Analyst', 'Excel, SQL, Python', 'Entry-level', 'Technology', '50000-80000'],
            ['Web Developer', 'HTML, CSS, JavaScript', 'Entry-level', 'Technology', '45000-75000']
        ]
        return pd.DataFrame(jobs, columns=['job_title', 'required_skills', 'experience_level', 'industry', 'salary_range'])

    def observe(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Step 1: Observe - Collect and structure user input data"""
        return {
            'timestamp': datetime.now().isoformat(),
            'user_profile': {
                'skills': user_data.get('skills', []),
                'interests': user_data.get('interests', []),
                'education': user_data.get('education', {}),
                'experience': user_data.get('experience', []),
                'preferences': user_data.get('preferences', {})
            },
            'context': {
                'location': user_data.get('location', 'Remote'),
                'salary_expectation': user_data.get('salary_expectation', 0),
                'employment_type': user_data.get('employment_type', 'Full-time'),
                'industry_preference': user_data.get('industry_preference', [])
            }
        }

    def understand(self, observed_data: Dict[str, Any]) -> Dict[str, Any]:
        """Step 2: Understand - Process and contextualize the observed data"""
        user_profile = observed_data['user_profile']
        context = observed_data['context']
        
        skill_profile = self._create_skill_profile(user_profile['skills'])
        experience_level = self._determine_experience_level(user_profile['experience'])
        career_domains = self._map_interests_to_domains(user_profile['interests'])
        
        return {
            'skill_profile': skill_profile,
            'experience_level': experience_level,
            'career_domains': career_domains,
            'user_context': context,
            'competency_score': self._calculate_competency_score(skill_profile, user_profile['education'])
        }

    def analyze(self, understanding: Dict[str, Any]) -> Dict[str, Any]:
        """Step 3: Analyze - Feature extraction and pattern recognition"""
        skill_vector = self._vectorize_skills(understanding['skill_profile'])
        market_analysis = self._analyze_job_market_fit(understanding['skill_profile'], understanding['career_domains'])
        skill_gaps = self._identify_skill_gaps(understanding['skill_profile'], understanding['career_domains'])
        
        return {
            'skill_vector': skill_vector,
            'market_compatibility': market_analysis,
            'skill_gaps': skill_gaps,
            'user_features': self._extract_user_features(understanding)
        }

    def reason(self, analyzed_features: Dict[str, Any]) -> Dict[str, Any]:
        """Step 4: Reason - Apply cognitive reasoning logic"""
        reasoning_factors = {
            'skill_match_score': self._calculate_skill_match_scores(analyzed_features),
            'career_progression_path': self._determine_career_progression(analyzed_features),
            'market_demand_analysis': self._analyze_market_demand(analyzed_features),
            'growth_potential': self._assess_growth_potential(analyzed_features)
        }
        
        reasoning_id = f"reasoning_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.reasoning_memory[reasoning_id] = reasoning_factors
        
        return {'reasoning_id': reasoning_id, 'factors': reasoning_factors}

    def decide(self, reasoning_results: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Step 5: Decide - Generate final job recommendations"""
        factors = reasoning_results['factors']
        recommendations = []
        
        for _, job in self.job_data.iterrows():
            job_score = self._calculate_job_score(job, factors)
            
            if job_score > 0.6:
                recommendations.append({
                    'job_title': job['job_title'],
                    'match_score': round(job_score, 2),
                    'required_skills': job['required_skills'],
                    'experience_level': job['experience_level'],
                    'industry': job['industry'],
                    'salary_range': job['salary_range'],
                    'reasoning_id': reasoning_results['reasoning_id']
                })
        
        recommendations.sort(key=lambda x: x['match_score'], reverse=True)
        return recommendations[:10]

    def explain(self, recommendations: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Step 6: Explain - Provide AI insights"""
        explanations = {}
        for rec in recommendations:
            reasoning_factors = self.reasoning_memory.get(rec['reasoning_id'], {})
            explanations[rec['job_title']] = {
                'why_recommended': self._generate_recommendation_explanation(rec, reasoning_factors),
                'skill_analysis': self._explain_skill_match(rec, reasoning_factors),
                'growth_opportunities': self._explain_growth_potential(rec, reasoning_factors),
                'improvement_suggestions': self._generate_improvement_suggestions(rec, reasoning_factors)
            }
        return explanations

    def learn(self, feedback_data: Dict[str, Any]):
        """Step 7: Learn - Store feedback for model fine-tuning"""
        self.user_feedback_history.append({
            'timestamp': datetime.now().isoformat(),
            'feedback': feedback_data,
            'user_id': feedback_data.get('user_id', 'anonymous')
        })

    # --- INTERNAL UTILITIES ---

    def _create_skill_profile(self, skills: List[str]) -> Dict[str, float]:
        return {skill.lower().strip(): 1.0 for skill in skills}

    def _determine_experience_level(self, experience: List[Dict]) -> str:
        total_years = sum([exp.get('years', 0) for exp in experience])
        if total_years < 2: return 'Entry-level'
        if total_years < 5: return 'Mid-level'
        return 'Senior-level'

    def _map_interests_to_domains(self, interests: List[str]) -> List[str]:
        mapping = {
            'technology': ['programming', 'coding', 'software', 'data', 'ai', 'web'],
            'design': ['design', 'creative', 'art', 'visual', 'ux', 'ui'],
            'business': ['management', 'strategy', 'finance', 'marketing']
        }
        domains = []
        for interest in interests:
            for domain, keywords in mapping.items():
                if any(kw in interest.lower() for kw in keywords):
                    if domain not in domains: domains.append(domain)
        return domains or ['technology']

    def _calculate_competency_score(self, skill_profile: Dict[str, float], education: Dict) -> float:
        skill_score = len(skill_profile) / 10.0
        edu_score = 0.5 + (0.1 * len(education.get('degrees', [])))
        return min(1.0, (skill_score + edu_score) / 2)

    def _vectorize_skills(self, skill_profile: Dict[str, float]) -> np.ndarray:
        if not SKLEARN_AVAILABLE or self.skill_vectorizer is None:
            return np.zeros(100)
        
        skills_text = ' '.join(skill_profile.keys())
        try:
            if hasattr(self.skill_vectorizer, 'vocabulary_'):
                return self.skill_vectorizer.transform([skills_text]).toarray()[0]
            return np.zeros(100)
        except Exception:
            return np.zeros(100)

    def _calculate_job_score(self, job: pd.Series, factors: Dict[str, Any]) -> float:
        title = job['job_title'].lower()
        category = 'technical_roles'
        if 'manager' in title or 'lead' in title: category = 'managerial_roles'
        elif 'design' in title or 'ux' in title: category = 'creative_roles'
            
        skill_score = factors['skill_match_score'].get(category, 0.5)
        market_demand = factors['market_demand_analysis'].get('high_demand_roles', 0.5)
        return float((skill_score * 0.7) + (market_demand * 0.3))

    def _identify_skill_gaps(self, skill_profile: Dict[str, float], domains: List[str]) -> List[str]:
        requirements = {'technology': ['python', 'sql', 'cloud'], 'design': ['figma', 'ux research']}
        gaps = []
        for domain in domains:
            for skill in requirements.get(domain, []):
                if skill not in skill_profile: gaps.append(skill)
        return list(set(gaps))

    def _extract_user_features(self, understanding: Dict[str, Any]) -> Dict[str, float]:
        return {'num_skills': len(understanding['skill_profile']), 'comp_score': understanding['competency_score']}

    def _calculate_skill_match_scores(self, features: Dict) -> Dict[str, float]:
        return {'technical_roles': 0.8, 'managerial_roles': 0.6, 'creative_roles': 0.5}

    def _determine_career_progression(self, features: Dict) -> List[str]:
        return ['Senior Specialist', 'Team Lead']

    def _analyze_market_demand(self, features: Dict) -> Dict[str, float]:
        return {'high_demand_roles': 0.85, 'traditional_roles': 0.6}

    def _assess_growth_potential(self, features: Dict) -> Dict[str, float]:
        return {'salary_growth': 0.8, 'skill_expansion': 0.9}

    def _generate_recommendation_explanation(self, rec: Dict, factors: Dict) -> str:
        return f"Matched {rec['job_title']} at {rec['match_score']*100}% based on your expertise."

    def _explain_skill_match(self, rec: Dict, factors: Dict) -> Dict[str, Any]:
        return {'matching': ['Core Skills'], 'gaps': ['Specialized Tools']}

    def _explain_growth_potential(self, rec: Dict, factors: Dict) -> Dict[str, Any]:
        return {'potential': 'High', 'path': 'Vertical'}

    def _generate_improvement_suggestions(self, rec: Dict, factors: Dict) -> List[str]:
        return ['Certify in relevant cloud technologies', 'Update portfolio']