"""
XAI Explainer
Provides narrative reasoning and visual-ready data for career insights.
"""

class XAIExplainer:
    
    @staticmethod
    def generate_xai_explanation(user_id, job_id, match_score, matched_skills, missing_skills, reasoning=None):
        job = Job.query.get(job_id)
        
        # If no reasoning is passed, auto-generate a narrative
        if not reasoning:
            reasoning = XAIExplainer._generate_narrative(matched_skills, missing_skills, job.job_title)

        explanation = {
            'overview': {
                'job_title': job.job_title if job else 'Unknown',
                'match_percentage': round(match_score, 1),
                'confidence': XAIExplainer._get_confidence_level(match_score),
            },
            'narrative': reasoning,
            'gap_analysis': {
                'strength_area': XAIExplainer._find_top_strength(matched_skills),
                'critical_gap': [s for s, d in missing_skills.items() if d['is_mandatory']],
                'upskilling_priority': "High" if any(d['is_mandatory'] for d in missing_skills.values()) else "Moderate"
            },
            'market_context': {
                'salary': job.average_salary,
                'demand': XAIExplainer._get_demand_description(job.job_market_demand),
                'growth': XAIExplainer._get_growth_potential(job.domain)
            }
        }
        return explanation

    @staticmethod
    def _generate_narrative(matched, missing, title):
        """Generates a human-like explanation of the match."""
        m_count = len(matched)
        critical_missing = [s for s, d in missing.items() if d['is_mandatory']]
        
        if m_count > 3 and not critical_missing:
            return f"You are an excellent candidate for {title}. Your core expertise aligns perfectly with the mandatory requirements."
        elif critical_missing:
            return f"You have a strong foundation, but {title} roles strictly require {', '.join(critical_missing)}. Focus on these to bridge the gap."
        return f"We found a moderate alignment. Enhancing your portfolio with the missing optional skills will significantly increase your competitiveness."

    @staticmethod
    def _find_top_strength(matched_skills):
        """Identifies the user's most relevant expert-level skill for this job."""
        experts = [name for name, d in matched_skills.items() if d['user_level'] == 'expert']
        return experts[0] if experts else "Foundational Skills"