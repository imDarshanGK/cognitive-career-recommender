"""
Cognitive Reasoning Engine
Rule-based reasoning for career recommendations
"""

from models import db, User, UserProfile, Job

class CognitiveReasoner:
    """
    Inference engine that generates justifications for recommendations.
    Uses templated logic to provide context-aware career advice.
    """
    
    # Domain-specific knowledge base
    REASONING_RULES = {
        'AI': {
            'primary': ['Python', 'Machine Learning', 'Deep Learning'],
            'template': 'Your mastery of {skills} makes you a competitive candidate for AI Research. The industry requires the exact neural network proficiency you demonstrate.'
        },
        'Data Science': {
            'primary': ['Python', 'Statistics', 'SQL'],
            'template': 'The transition to Data Science is supported by your analytical background in {skills}. Your ability to interpret complex datasets is a key differentiator.'
        },
        'Cloud': {
            'primary': ['AWS', 'Docker', 'Kubernetes'],
            'template': 'With infrastructure skills like {skills}, you are prepared for high-availability DevOps environments. Your profile suggests strong architectural awareness.'
        }
    }

    @staticmethod
    def generate_reasoning(user_id, job_id, matched_skills, match_score):
        """
        Synthesizes profile data and job requirements into a cohesive explanation.
        """
        user = db.session.get(User, user_id)
        job = db.session.get(Job, job_id)
        profile = UserProfile.query.filter_by(user_id=user_id).first()
        
        if not user or not job:
            return "Insufficient data to generate a custom career path reasoning."

        reasons = []

        # 1. Experience Level Context
        if profile and profile.experience_years:
            status = "perfectly aligns with" if str(job.experience_level).lower() in ['mid', 'senior'] and profile.experience_years > 3 else "is a solid entry point for"
            reasons.append(f"Your {profile.experience_years} years in the industry {status} this {job.experience_level} role.")

        # 2. Domain-Specific Inference
        domain_match = CognitiveReasoner.REASONING_RULES.get(job.domain)
        if domain_match:
            # Find which core domain skills the user actually has
            core_hits = [s for s in domain_match['primary'] if s.lower() in [k.lower() for k in matched_skills.keys()]]
            if core_hits:
                reasons.append(domain_match['template'].format(skills=', '.join(core_hits)))

        # 3. Quantitative Validation
        if match_score >= 80:
            reasons.append(f"At an {match_score}% match, your technical profile is in the top tier for this position.")
        
        return " ".join(reasons)

    @staticmethod
    def get_skill_gap_analysis(missing_skills):
        """
        Strategic reasoning for what the user should do next.
        """
        if not missing_skills:
            return "You meet all core requirements. Focus on your interview narrative."
        
        critical_gap = missing_skills[0]
        return f"To reach a 90%+ match, prioritizing the acquisition of '{critical_gap}' is your most effective next step."