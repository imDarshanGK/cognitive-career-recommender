"""
Roadmap Generator
Personalizes learning journeys based on the Cognitive Reasoner's gap analysis.
"""

class RoadmapGenerator:
    # ... (LEARNING_PATHS dictionary remains as defined)

    @staticmethod
    def generate_roadmap(job_domain, missing_skills):
        """
        Logic: Only show steps relevant to the user's gaps, but maintain 
        the logical order of learning.
        """
        base_path = RoadmapGenerator.LEARNING_PATHS.get(job_domain, [])
        
        if not base_path:
            return RoadmapGenerator._create_custom_roadmap(missing_skills)

        # Normalize missing skills for matching
        missing_skill_names = [s.strip().lower() for s in missing_skills.keys()]
        
        personalized_roadmap = []
        for step in base_path:
            # Check if this roadmap step covers any of the user's missing skills
            # or is a foundational 'Step 1' that they might need to review.
            is_relevant = any(
                part.strip().lower() in missing_skill_names 
                for part in step['skill'].replace('&', ',').split(',')
            )
            
            # Logic: Include the step if it's a gap, OR if it's highly 
            # critical to the domain's progression.
            if is_relevant or step['step'] == 1:
                # Flag the step if it contains a 'Mandatory' missing skill
                step['priority'] = 'High' if any(
                    missing_skills.get(k, {}).get('is_mandatory') 
                    for k in missing_skills if k.lower() in step['skill'].lower()
                ) else 'Standard'
                
                personalized_roadmap.append(step)

        return personalized_roadmap

    @staticmethod
    def _create_custom_roadmap(missing_skills):
        """
        For niche roles, create a dynamically generated list of learning goals.
        """
        # Sort so mandatory skills come first
        sorted_skills = sorted(
            missing_skills.items(), 
            key=lambda x: x[1].get('is_mandatory', False), 
            reverse=True
        )
        
        return [
            {
                'step': i + 1,
                'skill': name,
                'duration': '4 weeks',
                'difficulty': 'High' if details.get('required_level') == 'expert' else 'Medium',
                'priority': 'Mandatory' if details.get('is_mandatory') else 'Optional'
            }
            for i, (name, details) in enumerate(sorted_skills)
        ]