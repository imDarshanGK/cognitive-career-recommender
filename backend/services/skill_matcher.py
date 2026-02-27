"""
Skill Matching Engine
Calculates weighted scores based on presence, necessity, and proficiency.
"""

class SkillMatcher:
    # Numeric mapping for level-based comparison
    LEVEL_WEIGHTS = {
        'beginner': 1,
        'intermediate': 2,
        'expert': 3
    }

    @staticmethod
    def calculate_match_score(user_id, job_id):
        user_skills = {s.skill_name.lower(): s.skill_level.lower() 
                       for s in UserSkill.query.filter_by(user_id=user_id).all()}
        job_skills = JobSkill.query.filter_by(job_id=job_id).all()

        if not job_skills:
            return 0

        score_components = []
        mandatory_penalty = 0
        
        for js in job_skills:
            js_name = js.skill_name.lower()
            weight = 2.0 if js.is_mandatory else 1.0
            
            if js_name in user_skills:
                # 1. Base Match
                skill_score = 1.0
                
                # 2. Proficiency Adjustment
                user_lvl = SkillMatcher.LEVEL_WEIGHTS.get(user_skills[js_name], 1)
                req_lvl = SkillMatcher.LEVEL_WEIGHTS.get(js.required_level.lower(), 1)
                
                # If user level is lower than required, apply a slight penalty
                if user_lvl < req_lvl:
                    skill_score *= (user_lvl / req_lvl)
                
                score_components.append(skill_score * weight)
            else:
                # 3. Mandatory Check
                if js.is_mandatory:
                    mandatory_penalty += 0.15 # 15% flat deduction per missing mandatory skill
                score_components.append(0)

        # Calculate final weighted average
        total_possible_weight = sum(2.0 if js.is_mandatory else 1.0 for js in job_skills)
        base_score = (sum(score_components) / total_possible_weight) * 100
        
        # Apply mandatory penalties and clamp
        final_score = max(0, base_score - (mandatory_penalty * 100))
        return round(final_score, 2)