"""
Cognitive Reasoning Engine
Rule-based reasoning for career recommendations
"""

from models import User, UserProfile, UserSkill, Job

class CognitiveReasoner:
    """
    Cognitive reasoning engine
    Uses rule-based logic to explain recommendations
    """
    
    # Domain-specific rules
    REASONING_RULES = {
        'AI': {
            'primary_skills': ['Python', 'Machine Learning', 'Deep Learning'],
            'secondary_skills': ['Statistics', 'TensorFlow', 'PyTorch'],
            'domains': ['AI Research Engineer', 'Machine Learning Engineer', 'AI Research Engineer'],
            'reasoning_template': 'Your strong foundation in {skills} makes you well-suited for AI roles. The field of AI requires deep knowledge of machine learning algorithms and neural networks, where you demonstrate proficiency.'
        },
        'Data Science': {
            'primary_skills': ['Python', 'Statistics', 'Data Analysis', 'Machine Learning'],
            'secondary_skills': ['SQL', 'Pandas', 'Matplotlib'],
            'domains': ['Data Scientist', 'Data Analyst'],
            'reasoning_template': 'Your expertise in {skills} aligns perfectly with Data Science careers. You have the analytical foundation needed to extract insights from complex datasets.'
        },
        'Web': {
            'primary_skills': ['JavaScript', 'HTML', 'CSS'],
            'secondary_skills': ['React', 'Node.js', 'REST API'],
            'domains': ['Frontend Developer', 'Full Stack Developer', 'Backend Developer'],
            'reasoning_template': 'Your web development background with {skills} positions you well for web-based roles. The industry heavily demands these core technologies.'
        },
        'Cloud': {
            'primary_skills': ['AWS', 'Docker', 'Linux'],
            'secondary_skills': ['Kubernetes', 'Bash', 'Terraform'],
            'domains': ['Cloud Engineer', 'DevOps Engineer'],
            'reasoning_template': 'Your cloud infrastructure expertise in {skills} is highly relevant for cloud and DevOps positions. These are critical skills in modern software development.'
        }
    }
    
    @staticmethod
    def generate_reasoning(user_id, job_id, matched_skills, missing_skills, match_score):
        """
        Generate human-readable reasoning for a recommendation
        Returns: reasoning text
        """
        user = User.query.get(user_id)
        job = Job.query.get(job_id)
        user_profile = UserProfile.query.filter_by(user_id=user_id).first()
        
        if not user or not job:
            return "Unable to generate reasoning: missing data"
        
        reasoning_parts = []
        
        # 1. Experience alignment
        if user_profile and user_profile.experience_years:
            reasoning_parts.append(
                f"With {user_profile.experience_years} years of experience, you match the {job.experience_level} level requirements for this role."
            )
        
        # 2. Skill match reason
        if matched_skills:
            matched_list = ', '.join(matched_skills.keys())
            reasoning_parts.append(
                f"You possess key skills required: {matched_list}. These directly align with the job requirements."
            )
        
        # 3. Domain/field reasoning
        domain = job.domain
        if domain in CognitiveReasoner.REASONING_RULES:
            rule = CognitiveReasoner.REASONING_RULES[domain]
            skills_found = [s for s in rule['primary_skills'] if s.lower() in {k.lower() for k in matched_skills.keys()}]
            if skills_found:
                reasoning_parts.append(
                    f"In the {domain} domain, your expertise in {', '.join(skills_found)} is particularly valuable."
                )
        
        # 4. Score-based assessment
        if match_score >= 85:
            reasoning_parts.append(f"Your {match_score:.0f}% match score indicates an excellent fit for this role.")
        elif match_score >= 70:
            reasoning_parts.append(f"Your {match_score:.0f}% match score shows a strong alignment with this position.")
        elif match_score >= 50:
            reasoning_parts.append(f"Your {match_score:.0f}% match score suggests you have foundational skills for this role.")
        
        # 5. Job market demand
        reasoning_parts.append(
            f"This role has a market demand rating of {job.job_market_demand}/10, indicating strong industry need."
        )
        
        return ' '.join(reasoning_parts)
    
    @staticmethod
    def get_skill_level_assessment(matched_skills):
        """
        Assess overall skill level based on matched skills
        Returns: (level, description)
        """
        if not matched_skills:
            return "novice", "You are new to this field"
        
        expert_count = sum(1 for s in matched_skills.values() if s['user_level'] == 'expert')
        intermediate_count = sum(1 for s in matched_skills.values() if s['user_level'] == 'intermediate')
        
        total = len(matched_skills)
        expert_ratio = expert_count / total
        
        if expert_ratio >= 0.7:
            return "expert", "You have deep expertise in this area"
        elif expert_ratio >= 0.4 or intermediate_count >= total * 0.7:
            return "intermediate", "You have solid foundational knowledge"
        else:
            return "beginner", "You have basic knowledge in this area"
