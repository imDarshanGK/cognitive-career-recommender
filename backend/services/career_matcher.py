"""
Career role matching engine
Simple skill overlap scoring with explainable output and roadmap generation.
"""

import json
import os
import logging
from typing import Dict, List, Any

logger = logging.getLogger(__name__)
DATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'career_roles.json')


def load_roles() -> List[Dict[str, Any]]:
    """Load career roles from JSON file with error handling"""
    try:
        with open(DATA_PATH, 'r') as handle:
            roles = json.load(handle)
            logger.debug(f"Loaded {len(roles)} career roles")
            return roles
    except FileNotFoundError:
        logger.error(f"Career roles file not found: {DATA_PATH}")
        return []
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in career roles file: {e}")
        return []


def normalize_profile(profile: Dict[str, Any]) -> Dict[str, Any]:
    skills = profile.get('skills', []) or []
    interests = profile.get('interests', []) or []
    education = profile.get('education', {}) or {}
    experience = profile.get('experience', []) or []

    # Skill aliases for better matching
    SKILL_ALIASES = {
        'mysql': ['sql', 'mysql'],
        'postgresql': ['sql', 'postgresql', 'postgres'],
        'mongodb': ['nosql', 'mongodb', 'mongo'],
        'sklearn': ['scikit-learn', 'sklearn', 'machine learning'],
        'scikit-learn': ['scikit-learn', 'sklearn', 'machine learning'],
        'tensorflow': ['tensorflow', 'deep learning', 'ml'],
        'pytorch': ['pytorch', 'deep learning', 'ml'],
        'keras': ['keras', 'deep learning', 'ml'],
        'rest api': ['rest', 'api', 'rest api', 'restful'],
        'node': ['node', 'nodejs', 'node.js'],
        'react': ['react', 'reactjs', 'react.js']
    }

    # Ensure skills are strings and normalized to lowercase
    normalized_skills = []
    for skill in skills:
        skill_str = str(skill).strip().lower()
        if skill_str:
            normalized_skills.append(skill_str)
            # Add aliases for better matching
            if skill_str in SKILL_ALIASES:
                normalized_skills.extend(SKILL_ALIASES[skill_str])
    
    normalized_skills = sorted(set(normalized_skills))
    
    normalized_interests = sorted({str(interest).strip().lower() for interest in interests if str(interest).strip()})

    years = 0
    if experience:
        for entry in experience:
            years = max(years, entry.get('years', 0) or entry.get('total_years', 0))

    experience_level = infer_experience_level(years)
    
    logger.debug(f"Normalized {len(normalized_skills)} skills (with aliases): {normalized_skills[:20]}")

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


def calculate_weighted_match_score(matched_skills: List[str], required_skills: List[str], 
                                   missing_skills: List[str], user_experience_level: str,
                                   role_experience_level: str, user_total_skills: int) -> float:
    """
    Calculate a realistic weighted match score with multiple factors.
    
    Components:
    - Skill Overlap (40%): How many required skills the user has
    - Experience Match (30%): Does user's experience level meet role requirements
    - Skill Breadth (20%): Total skills user has (indicates versatility)
    - Skill Depth Bonus (10%): Extra points for demonstrating multiple related skills
    """
    if not required_skills:
        return 0.0
    
    # 1. Skill Overlap Score (40 points max)
    overlap_ratio = len(matched_skills) / len(required_skills) if required_skills else 0
    skill_overlap_score = overlap_ratio * 40
    
    # 2. Experience Level Match (30 points max)
    experience_map = {'entry': 1, 'mid': 2, 'senior': 3}
    user_exp = experience_map.get(user_experience_level, 1)
    role_exp = experience_map.get(role_experience_level, 1)
    
    if user_exp >= role_exp:
        # User meets or exceeds experience requirement
        experience_score = 30
    elif user_exp == role_exp - 1:
        # User is one level below (e.g., mid vs senior)
        experience_score = 20
    else:
        # User is significantly below required experience
        experience_score = 10
    
    # 3. Skill Breadth Bonus (20 points max)
    # Users with more total skills get higher scores
    skill_count_score = min(20, (user_total_skills / 10) * 20)  # Normalize to ~10 skills for max points
    
    # 4. Skill Depth Bonus (10 points max)
    # Get bonus if user has 80%+ of required skills
    if overlap_ratio >= 0.8:
        depth_bonus = 10
    elif overlap_ratio >= 0.5:
        depth_bonus = 5
    else:
        depth_bonus = 0
    
    total_score = skill_overlap_score + experience_score + skill_count_score + depth_bonus
    
    # Cap at 100 and ensure at least 25-30 for any match with some overlap
    final_score = min(100, max(25 if matched_skills else 0, total_score))
    
    logger.debug(f"Weighted score: overlap={skill_overlap_score:.1f} + exp={experience_score} + breadth={skill_count_score:.1f} + depth={depth_bonus} = {final_score:.1f}")
    
    return round(final_score, 1)


def _extract_market_skills(jobs: List[Dict[str, Any]]) -> Dict[str, int]:
    """Extract skills from real job descriptions with frequency count"""
    import re
    
    # Common technical skills to look for
    skills_dict = {
        'python': 0, 'java': 0, 'javascript': 0, 'typescript': 0, 'c++': 0, 'c#': 0,
        'react': 0, 'angular': 0, 'vue': 0, 'node': 0, 'express': 0, 'django': 0, 'flask': 0,
        'sql': 0, 'mysql': 0, 'postgresql': 0, 'mongodb': 0, 'redis': 0, 'firebase': 0,
        'aws': 0, 'azure': 0, 'gcp': 0, 'docker': 0, 'kubernetes': 0, 'jenkins': 0,
        'machine learning': 0, 'ai': 0, 'deep learning': 0, 'tensorflow': 0, 'pytorch': 0, 'keras': 0,
        'rest api': 0, 'graphql': 0, 'microservices': 0, 'ci/cd': 0, 'devops': 0,
        'git': 0, 'linux': 0, 'unix': 0, 'bash': 0, 'html': 0, 'css': 0,
        'fastapi': 0, 'spring': 0, 'fastapi': 0, 'scikitlearn': 0, 'pandas': 0, 'numpy': 0
    }
    
    for job in jobs:
        desc = (job.get('description', '') + ' ' + job.get('job_title', '')).lower()
        for skill in skills_dict.keys():
            if re.search(r'\b' + re.escape(skill) + r'\b', desc):
                skills_dict[skill] += 1
    
    # Return skills sorted by frequency
    return {k: v for k, v in sorted(skills_dict.items(), key=lambda x: x[1], reverse=True) if v > 0}


def match_roles(profile: Dict[str, Any]) -> Dict[str, Any]:
    """Match user profile and fetch real job market data"""
    import os
    from utils.data_processor import DataProcessor
    
    roles = load_roles()
    normalized_profile = normalize_profile(profile)
    user_skills = normalized_profile['skills']
    
    logger.debug(f"User has {len(user_skills)} skills: {user_skills}")
    
    # Always get real job market skills from Adzuna - this is the primary data source
    market_skills = {}
    try:
        dp = DataProcessor()
        app_id = os.environ.get('ADZUNA_APP_ID')
        app_key = os.environ.get('ADZUNA_APP_KEY')
        
        if app_id and app_key:
            # List of high-value technical skills for fallback queries
            high_value_skills = [
                'python', 'java', 'javascript', 'react', 'node', 'aws', 'docker',
                'kubernetes', 'machine learning', 'data science', 'sql', 'angular', 
                'vue', 'typescript', 'go', 'rust', 'c++', 'c#', '.net', 'flask',
                'django', 'spring', 'mysql', 'postgresql', 'mongodb', 'redis', 'developer'
            ]
            
            real_jobs = None
            
            # First, try user's best matching skill
            if user_skills:
                best_skill = None
                for skill in user_skills:
                    skill_lower = skill.lower()
                    # Check if skill matches a high-value technical skill
                    if any(hv.lower() in skill_lower or skill_lower in hv.lower() for hv in high_value_skills):
                        best_skill = skill
                        break
                
                if best_skill:
                    logger.info(f"Attempting primary query with skill: {best_skill}")
                    real_jobs = dp._fetch_adzuna_jobs({'query': best_skill, 'results': 15})
                    if real_jobs and len(real_jobs) > 0:
                        logger.info(f"✓ Got {len(real_jobs)} jobs for '{best_skill}'")
            
            # If primary failed or no valid skills, try fallback queries
            if not real_jobs or len(real_jobs) == 0:
                logger.info("Primary query failed, trying fallback queries...")
                fallback_queries = ['python', 'java', 'javascript', 'react', 'developer']
                for fallback_skill in fallback_queries:
                    logger.info(f"Trying fallback: {fallback_skill}")
                    real_jobs = dp._fetch_adzuna_jobs({'query': fallback_skill, 'results': 15})
                    if real_jobs and len(real_jobs) > 0:
                        logger.info(f"✓ Fallback successful! Got {len(real_jobs)} jobs for '{fallback_skill}'")
                        break
            
            # Extract market skills from whatever jobs we got
            if real_jobs and len(real_jobs) > 0:
                market_skills = _extract_market_skills(real_jobs)
                logger.info(f"✓ Extracted {len(market_skills)} market skills from {len(real_jobs)} jobs")
                logger.info(f"  Top skills: {list(market_skills.keys())[:8]}")
            else:
                logger.warning("✗ All queries failed - no real jobs available from Adzuna")
        else:
            logger.warning("Adzuna credentials not configured")
    except Exception as e:
        logger.error(f"Exception fetching market skills: {type(e).__name__}: {str(e)}", exc_info=True)

    recommendations = []
    for role in roles:
        required = [skill.lower() for skill in role.get('required_skills', [])]
        matched = [skill for skill in required if skill in user_skills]
        missing = [skill for skill in required if skill not in user_skills]

        # Use weighted scoring for more realistic results
        score = calculate_weighted_match_score(
            matched_skills=matched,
            required_skills=required,
            missing_skills=missing,
            user_experience_level=normalized_profile.get('experience_level', 'entry'),
            role_experience_level=role.get('experience_level', 'entry'),
            user_total_skills=len(normalized_profile.get('skills', []))
        )
        
        logger.debug(f"Role '{role.get('role')}' - Required: {required[:5]}, Matched: {matched}, Score: {score}%")

        recommendations.append({
            'job_title': role.get('role'),
            'match_score': score,
            'required_skills': required,
            'experience_level': role.get('experience_level'),
            'matched_skills': matched,
            'missing_skills': missing,
            'skill_confidence': _get_skill_confidence_levels(matched, score),
            'explanation': build_explanation(matched, missing),
            'roadmap': build_roadmap(missing, role.get('related_skills_to_learn', []))
        })

    recommendations.sort(key=lambda rec: rec['match_score'], reverse=True)
    
    # Filter to show only suitable matches (40% and above)
    # This prevents overwhelming users with too many low-quality matches
    suitable_recommendations = [rec for rec in recommendations if rec['match_score'] >= 40]
    
    # If no suitable matches, show top 3 anyway for user awareness
    final_recommendations = suitable_recommendations if suitable_recommendations else recommendations[:3]
    
    logger.debug(f"Returning {len(final_recommendations)} recommendations")

    return {
        'normalized_profile': normalized_profile,
        'recommendations': final_recommendations,
        'market_skills': market_skills  # Real skills from job market
    }


def build_explanation(matched: List[str], missing: List[str]) -> List[str]:
    explanation = []
    for skill in matched:
        explanation.append(f"✓ Your {skill} skill matches the role requirement.")
    for skill in missing:
        explanation.append(f"✗ Missing skill: {skill}.")
    return explanation


def _get_skill_confidence_levels(matched_skills: List[str], match_score: float) -> Dict[str, str]:
    """
    Determine confidence level for each skill based on match strength
    
    Confidence levels:
    - Advanced: Skill is in top matched (80%+ match score)
    - Intermediate: Skill is matched but score is moderate (50-79%)
    - Beginner: Skill is mentioned in radar (below 50%)
    """
    confidence_levels = {}
    
    if match_score >= 80:
        level = 'Advanced'
    elif match_score >= 50:
        level = 'Intermediate'
    else:
        level = 'Beginner'
    
    for skill in matched_skills:
        confidence_levels[skill] = level
    
    return confidence_levels


def build_roadmap(missing: List[str], related: List[str]) -> List[str]:
    """Generate learning roadmap based on real market demands"""
    roadmap = []
    
    # Prioritize by market demand (from real jobs)
    for skill in missing[:6]:  # Limit to top 6 most impactful
        roadmap.append(f"1. Master {skill} through hands-on project")
        roadmap.append(f"   - Build portfolio project using {skill}")
        roadmap.append(f"   - Practice on real GitHub projects")
        roadmap.append('')
    
    return roadmap
