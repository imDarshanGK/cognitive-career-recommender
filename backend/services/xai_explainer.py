"""
Explainable AI (XAI) Module
Generates explanations for recommendations
"""

import json
from models import Recommendation, User, Job

class XAIExplainer:
    """
    Generate explainable AI insights
    Provides transparent reasoning for recommendations
    """
    
    @staticmethod
    def generate_xai_explanation(user_id, job_id, match_score, matched_skills, missing_skills, reasoning):
        """
        Generate comprehensive XAI explanation
        Returns: dict with explanation details
        """
        job = Job.query.get(job_id)
        
        explanation = {
            'recommendation': {
                'job_title': job.job_title if job else 'Unknown',
                'match_percentage': round(match_score, 1),
                'confidence_level': XAIExplainer._get_confidence_level(match_score)
            },
            'why_recommended': reasoning,
            'skill_analysis': {
                'matched': {
                    'count': len(matched_skills),
                    'skills': list(matched_skills.keys()),
                    'details': matched_skills
                },
                'missing': {
                    'count': len(missing_skills),
                    'critical': [s for s, d in missing_skills.items() if d['is_mandatory']],
                    'optional': [s for s, d in missing_skills.items() if not d['is_mandatory']],
                    'details': missing_skills
                },
                'skill_gap': len(missing_skills) - sum(1 for d in missing_skills.values() if not d['is_mandatory'])
            },
            'market_insights': {
                'demand_level': XAIExplainer._get_demand_description(job.job_market_demand) if job else 'Unknown',
                'salary_range': job.average_salary if job else 'Unknown',
                'growth_potential': XAIExplainer._get_growth_potential(job.domain) if job else 'Unknown'
            }
        }
        
        return explanation
    
    @staticmethod
    def _get_confidence_level(score):
        """Convert score to confidence level"""
        if score >= 85:
            return "Very High"
        elif score >= 70:
            return "High"
        elif score >= 50:
            return "Moderate"
        else:
            return "Low"
    
    @staticmethod
    def _get_demand_description(demand_score):
        """Convert demand score to description"""
        if demand_score >= 9:
            return "Extremely High (9+/10)"
        elif demand_score >= 8:
            return "Very High (8-9/10)"
        elif demand_score >= 7:
            return "High (7-8/10)"
        else:
            return "Moderate (Below 7/10)"
    
    @staticmethod
    def _get_growth_potential(domain):
        """Get growth potential based on domain"""
        growth_map = {
            'AI': 'Exceptional - Fastest growing tech domain',
            'Data Science': 'Exceptional - Data is the new oil',
            'Cloud': 'Very Strong - Cloud adoption accelerating',
            'Web': 'Strong - Core to digital transformation',
            'Enterprise': 'Stable - Reliable long-term opportunities'
        }
        return growth_map.get(domain, 'Strong - Growing field')
