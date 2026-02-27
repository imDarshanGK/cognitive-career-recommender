def build_roadmap(missing: List[str], related: List[str]) -> List[Dict[str, Any]]:
    """
    Generate a structured learning roadmap.
    Transformed from a flat list to a structured object for better UI rendering.
    """
    structured_roadmap = []
    
    # Focus on the most critical gaps
    priority_skills = missing[:4]
    
    for i, skill in enumerate(priority_skills, 1):
        step = {
            "phase": f"Phase {i}: {skill.title()} Mastery",
            "actions": [
                f"Complete a specialized project using {skill}",
                f"Contribute to an open-source repository featuring {skill}",
                f"Review {skill} documentation for best practices"
            ],
            "estimated_time": "2-4 Weeks"
        }
        structured_roadmap.append(step)
    
    return structured_roadmap

def build_explanation(matched: List[str], missing: List[str]) -> Dict[str, List[str]]:
    """
    Categorized explanation for clearer 'Explainable AI' (XAI) output.
    """
    return {
        "strengths": [f"✓ High compatibility with {s}" for s in matched[:3]],
        "gaps": [f"✗ Bridge your knowledge in {s}" for s in missing[:3]],
        "summary": f"You match {len(matched)} core requirements for this role."
    }