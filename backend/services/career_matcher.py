"""
Career role matching engine
Simple skill overlap scoring with explainable output and roadmap generation.
"""

import json
import os
from typing import Dict, List, Any

DATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'career_roles.json')


def load_roles() -> List[Dict[str, Any]]:
    with open(DATA_PATH, 'r') as handle:
        return json.load(handle)


def normalize_profile(profile: Dict[str, Any]) -> Dict[str, Any]:
    skills = profile.get('skills', []) or []
    interests = profile.get('interests', []) or []
    education = profile.get('education', {}) or {}
    experience = profile.get('experience', []) or []

    normalized_skills = sorted({str(skill).strip().lower() for skill in skills if str(skill).strip()})
    normalized_interests = sorted({str(interest).strip().lower() for interest in interests if str(interest).strip()})

    years = 0
    if experience:
        for entry in experience:
            years = max(years, entry.get('years', 0) or entry.get('total_years', 0))

    experience_level = infer_experience_level(years)

    return {
        'skills': normalized_skills,
        'interests': normalized_interests,
        'education': education,
        'experience_level': experience_level,
        'years_experience': years
    }


def infer_experience_level(years: float) -> str:
    if years < 2:
        return 'entry'
    if years < 5:
        return 'mid'
    return 'senior'


def match_roles(profile: Dict[str, Any]) -> Dict[str, Any]:
    roles = load_roles()
    normalized_profile = normalize_profile(profile)
    user_skills = normalized_profile['skills']

    recommendations = []
    for role in roles:
        required = [skill.lower() for skill in role.get('required_skills', [])]
        matched = [skill for skill in required if skill in user_skills]
        missing = [skill for skill in required if skill not in user_skills]

        score = 0
        if required:
            score = round((len(matched) / len(required)) * 100, 1)

        recommendations.append({
            'job_title': role.get('role'),
            'match_score': score,
            'required_skills': required,
            'experience_level': role.get('experience_level'),
            'matched_skills': matched,
            'missing_skills': missing,
            'explanation': build_explanation(matched, missing),
            'roadmap': build_roadmap(missing, role.get('related_skills_to_learn', []))
        })

    recommendations.sort(key=lambda rec: rec['match_score'], reverse=True)

    return {
        'normalized_profile': normalized_profile,
        'recommendations': recommendations
    }


def build_explanation(matched: List[str], missing: List[str]) -> List[str]:
    explanation = []
    for skill in matched:
        explanation.append(f"Your {skill} skill matches the role requirement.")
    for skill in missing:
        explanation.append(f"Missing skill: {skill}.")
    return explanation


def build_roadmap(missing: List[str], related: List[str]) -> List[str]:
    roadmap = []
    for skill in missing:
        roadmap.append(f"Learn {skill}")
    for skill in related:
        if skill not in missing:
            roadmap.append(f"Explore {skill}")
    return roadmap
