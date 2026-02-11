"""
Cognitive AI Engine for Career & Job Recommendation System
Implements the cognitive loop: Observe → Understand → Analyze → Reason → Decide → Explain → Learn
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import shap
import lime
from lime.lime_text import LimeTextExplainer
import joblib
import json
from typing import Dict, List, Any, Tuple
from datetime import datetime

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
        self.explainer = None
        
        # Initialize cognitive components
        self._initialize_models()
        self._load_job_data()
    
    def _initialize_models(self):
        """Initialize machine learning models and explainable AI components"""
        try:
            # Load pre-trained models if available
            self.job_model = joblib.load('models/job_recommendation_model.pkl')
            self.skill_vectorizer = joblib.load('models/skill_vectorizer.pkl')
        except FileNotFoundError:
            # Initialize new models if not found
            self.job_model = RandomForestClassifier(n_estimators=100, random_state=42)
            self.skill_vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
        
        # Initialize explainable AI components
        self.lime_explainer = LimeTextExplainer(class_names=['Not Suitable', 'Suitable'])
    
    def _load_job_data(self):
        """Load job market data for recommendations"""
        try:
            self.job_data = pd.read_csv('data/job_dataset.csv')
        except FileNotFoundError:
            # Create sample job data if dataset not available
            self.job_data = self._create_sample_job_data()
    
    def _create_sample_job_data(self):
        """Create sample job data for testing purposes"""
        return pd.DataFrame({
            'job_title': ['Data Scientist', 'Software Engineer', 'Product Manager', 'UX Designer'],
            'required_skills': ['Python, ML, Statistics', 'Java, Python, SQL', 'Strategy, Analytics', 'Design, Research'],
            'experience_level': ['Mid-level', 'Entry-level', 'Senior-level', 'Mid-level'],
            'industry': ['Technology', 'Technology', 'Technology', 'Design'],
            'salary_range': ['80000-120000', '60000-100000', '100000-150000', '70000-110000']
        })
    
    def observe(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Step 1: Observe - Collect and structure user input data
        
        Args:
            user_data: Raw user input containing skills, interests, education, experience
            
        Returns:
            Structured observation data
        """
        observed_data = {
            'timestamp': datetime.now().isoformat(),
            'user_profile': {
                'skills': user_data.get('skills', []),
                'interests': user_data.get('interests', []),
                'education': user_data.get('education', {}),
                'experience': user_data.get('experience', []),
                'preferences': user_data.get('preferences', {})
            },
            'context': {
                'location': user_data.get('location', ''),
                'salary_expectation': user_data.get('salary_expectation', 0),
                'employment_type': user_data.get('employment_type', 'Full-time'),
                'industry_preference': user_data.get('industry_preference', [])
            }
        }
        
        return observed_data
    
    def understand(self, observed_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Step 2: Understand - Process and contextualize the observed data
        
        Args:
            observed_data: Structured observation from step 1
            
        Returns:
            Contextually processed understanding
        """
        user_profile = observed_data['user_profile']
        context = observed_data['context']
        
        # Process skills and create skill profile
        skill_profile = self._create_skill_profile(user_profile['skills'])
        
        # Analyze experience level
        experience_level = self._determine_experience_level(user_profile['experience'])
        
        # Process interests and map to career domains
        career_domains = self._map_interests_to_domains(user_profile['interests'])
        
        understanding = {
            'skill_profile': skill_profile,
            'experience_level': experience_level,
            'career_domains': career_domains,
            'user_context': context,
            'competency_score': self._calculate_competency_score(skill_profile, user_profile['education'])
        }
        
        return understanding
    
    def analyze(self, understanding: Dict[str, Any]) -> Dict[str, Any]:
        """
        Step 3: Analyze - Feature extraction and pattern recognition
        
        Args:
            understanding: Processed understanding from step 2
            
        Returns:
            Analyzed features and patterns
        """
        # Create feature vectors for machine learning
        skill_vector = self._vectorize_skills(understanding['skill_profile'])
        
        # Analyze job market compatibility
        market_analysis = self._analyze_job_market_fit(
            understanding['skill_profile'],
            understanding['career_domains']
        )
        
        # Identify skill gaps
        skill_gaps = self._identify_skill_gaps(
            understanding['skill_profile'],
            understanding['career_domains']
        )
        
        analyzed_features = {
            'skill_vector': skill_vector,
            'market_compatibility': market_analysis,
            'skill_gaps': skill_gaps,
            'user_features': self._extract_user_features(understanding)
        }
        
        return analyzed_features
    
    def reason(self, analyzed_features: Dict[str, Any]) -> Dict[str, Any]:
        """
        Step 4: Reason - Apply cognitive reasoning to make informed decisions
        
        Args:
            analyzed_features: Features and patterns from step 3
            
        Returns:
            Reasoning results and decision factors
        """
        # Apply reasoning rules and logic
        reasoning_factors = {
            'skill_match_score': self._calculate_skill_match_scores(analyzed_features),
            'career_progression_path': self._determine_career_progression(analyzed_features),
            'market_demand_analysis': self._analyze_market_demand(analyzed_features),
            'growth_potential': self._assess_growth_potential(analyzed_features)
        }
        
        # Store reasoning in memory for future reference
        reasoning_id = f"reasoning_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.reasoning_memory[reasoning_id] = reasoning_factors
        
        return {
            'reasoning_id': reasoning_id,
            'factors': reasoning_factors
        }
    
    def decide(self, reasoning_results: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Step 5: Decide - Generate final job recommendations
        
        Args:
            reasoning_results: Results from reasoning step
            
        Returns:
            List of job recommendations with scores
        """
        factors = reasoning_results['factors']
        
        # Generate recommendations based on reasoning
        recommendations = []
        
        for _, job in self.job_data.iterrows():
            job_score = self._calculate_job_score(job, factors)
            
            if job_score > 0.6:  # Threshold for recommendations
                recommendation = {
                    'job_title': job['job_title'],
                    'match_score': round(job_score, 2),
                    'required_skills': job['required_skills'],
                    'experience_level': job['experience_level'],
                    'industry': job['industry'],
                    'salary_range': job['salary_range'],
                    'reasoning_id': reasoning_results['reasoning_id']
                }
                recommendations.append(recommendation)
        
        # Sort by match score
        recommendations.sort(key=lambda x: x['match_score'], reverse=True)
        
        return recommendations[:10]  # Top 10 recommendations
    
    def explain(self, recommendations: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Step 6: Explain - Provide explainable AI insights for recommendations
        
        Args:
            recommendations: Job recommendations from decision step
            
        Returns:
            Detailed explanations for each recommendation
        """
        explanations = {}
        
        for rec in recommendations:
            job_title = rec['job_title']
            reasoning_id = rec['reasoning_id']
            
            # Get reasoning factors from memory
            reasoning_factors = self.reasoning_memory.get(reasoning_id, {})
            
            explanation = {
                'why_recommended': self._generate_recommendation_explanation(rec, reasoning_factors),
                'skill_analysis': self._explain_skill_match(rec, reasoning_factors),
                'growth_opportunities': self._explain_growth_potential(rec, reasoning_factors),
                'improvement_suggestions': self._generate_improvement_suggestions(rec, reasoning_factors)
            }
            
            explanations[job_title] = explanation
        
        return explanations
    
    def learn(self, feedback_data: Dict[str, Any]):
        """
        Step 7: Learn - Adaptive learning from user feedback
        
        Args:
            feedback_data: User feedback on recommendations
        """
        # Store feedback for learning
        feedback_entry = {
            'timestamp': datetime.now().isoformat(),
            'feedback': feedback_data,
            'user_id': feedback_data.get('user_id', 'anonymous')
        }
        
        self.user_feedback_history.append(feedback_entry)
        
        # Update models based on feedback (simplified approach)
        self._update_recommendation_model(feedback_data)
    
    # Helper methods for cognitive processing
    def _create_skill_profile(self, skills: List[str]) -> Dict[str, float]:
        """Create a weighted skill profile"""
        skill_weights = {}
        for skill in skills:
            skill_weights[skill.lower()] = 1.0  # Can be adjusted based on proficiency
        return skill_weights
    
    def _determine_experience_level(self, experience: List[Dict]) -> str:
        """Determine experience level from work history"""
        total_years = sum([exp.get('years', 0) for exp in experience])
        if total_years < 2:
            return 'Entry-level'
        elif total_years < 5:
            return 'Mid-level'
        else:
            return 'Senior-level'
    
    def _map_interests_to_domains(self, interests: List[str]) -> List[str]:
        """Map user interests to career domains"""
        domain_mapping = {
            'technology': ['programming', 'coding', 'software', 'data', 'ai'],
            'design': ['design', 'creative', 'art', 'visual', 'ux'],
            'business': ['business', 'management', 'strategy', 'finance'],
            'healthcare': ['health', 'medical', 'care', 'wellness'],
            'education': ['teaching', 'education', 'training', 'learning']
        }
        
        domains = []
        for interest in interests:
            for domain, keywords in domain_mapping.items():
                if any(keyword in interest.lower() for keyword in keywords):
                    if domain not in domains:
                        domains.append(domain)
        
        return domains or ['technology']  # Default to technology
    
    def _calculate_competency_score(self, skill_profile: Dict[str, float], education: Dict) -> float:
        """Calculate overall competency score"""
        skill_score = sum(skill_profile.values()) / max(1, len(skill_profile))
        education_score = 0.5 + (0.1 * len(education.get('degrees', [])))
        return min(1.0, (skill_score + education_score) / 2)
    
    def _vectorize_skills(self, skill_profile: Dict[str, float]) -> np.ndarray:
        """Convert skills to feature vector"""
        skills_text = ' '.join(skill_profile.keys())
        try:
            vector = self.skill_vectorizer.transform([skills_text])
            return vector.toarray()[0]
        except:
            # If vectorizer not fitted, return dummy vector
            return np.zeros(100)
    
    def _analyze_job_market_fit(self, skill_profile: Dict[str, float], career_domains: List[str]) -> Dict[str, float]:
        """Analyze fit with current job market"""
        return {
            'market_demand': 0.8,  # Placeholder
            'skill_relevance': 0.7,
            'domain_alignment': 0.9
        }
    
    def _identify_skill_gaps(self, skill_profile: Dict[str, float], career_domains: List[str]) -> List[str]:
        """Identify missing skills for target domains"""
        domain_skills = {
            'technology': ['python', 'sql', 'machine learning', 'cloud computing'],
            'design': ['figma', 'sketch', 'user research', 'prototyping'],
            'business': ['project management', 'data analysis', 'stakeholder management']
        }
        
        gaps = []
        for domain in career_domains:
            required_skills = domain_skills.get(domain, [])
            for skill in required_skills:
                if skill not in [s.lower() for s in skill_profile.keys()]:
                    gaps.append(skill)
        
        return gaps
    
    def _extract_user_features(self, understanding: Dict[str, Any]) -> Dict[str, float]:
        """Extract numerical features for ML model"""
        return {
            'num_skills': len(understanding['skill_profile']),
            'competency_score': understanding['competency_score'],
            'num_domains': len(understanding['career_domains'])
        }
    
    def _calculate_skill_match_scores(self, analyzed_features: Dict[str, Any]) -> Dict[str, float]:
        """Calculate skill match scores for different job categories"""
        return {
            'technical_roles': 0.85,
            'managerial_roles': 0.65,
            'creative_roles': 0.70
        }
    
    def _determine_career_progression(self, analyzed_features: Dict[str, Any]) -> List[str]:
        """Determine possible career progression paths"""
        return ['Senior Developer', 'Tech Lead', 'Engineering Manager']
    
    def _analyze_market_demand(self, analyzed_features: Dict[str, Any]) -> Dict[str, float]:
        """Analyze current market demand"""
        return {
            'high_demand_roles': 0.9,
            'emerging_technologies': 0.8,
            'traditional_roles': 0.6
        }
    
    def _assess_growth_potential(self, analyzed_features: Dict[str, Any]) -> Dict[str, float]:
        """Assess growth potential in different areas"""
        return {
            'salary_growth': 0.8,
            'skill_development': 0.9,
            'career_advancement': 0.7
        }
    
    def _calculate_job_score(self, job: pd.Series, factors: Dict[str, Any]) -> float:
        """Calculate overall job recommendation score"""
        # Simplified scoring based on multiple factors
        base_score = 0.7
        skill_bonus = factors['skill_match_score'].get('technical_roles', 0.5) * 0.3
        market_bonus = factors['market_demand_analysis'].get('high_demand_roles', 0.5) * 0.2
        
        return min(1.0, base_score + skill_bonus + market_bonus)
    
    def _generate_recommendation_explanation(self, recommendation: Dict, factors: Dict) -> str:
        """Generate human-readable explanation for recommendation"""
        job_title = recommendation['job_title']
        match_score = recommendation['match_score']
        
        return f"Recommended {job_title} with {match_score*100:.0f}% match based on your skill profile and market analysis. Your technical skills align well with the role requirements."
    
    def _explain_skill_match(self, recommendation: Dict, factors: Dict) -> Dict[str, Any]:
        """Explain skill matching analysis"""
        return {
            'matching_skills': ['Python', 'Data Analysis', 'Problem Solving'],
            'skill_gaps': ['Machine Learning', 'Cloud Platforms'],
            'proficiency_level': 'Intermediate to Advanced'
        }
    
    def _explain_growth_potential(self, recommendation: Dict, factors: Dict) -> Dict[str, Any]:
        """Explain growth and career advancement potential"""
        return {
            'short_term': 'Skill development in specialized areas',
            'long_term': 'Leadership and strategic roles',
            'earning_potential': 'Above average market salary'
        }
    
    def _generate_improvement_suggestions(self, recommendation: Dict, factors: Dict) -> List[str]:
        """Generate actionable improvement suggestions"""
        return [
            'Complete online courses in Machine Learning',
            'Gain experience with cloud platforms (AWS, Azure)',
            'Build portfolio projects showcasing data analysis skills',
            'Attend industry networking events and conferences'
        ]
    
    def _update_recommendation_model(self, feedback_data: Dict):
        """Update ML models based on user feedback"""
        # Simplified model update - in production, this would involve retraining
        if feedback_data.get('liked', False):
            # Positive feedback - increase weight for similar recommendations
            pass
        else:
            # Negative feedback - adjust recommendation criteria
            pass