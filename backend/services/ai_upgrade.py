"""Advanced AI helpers for speech profile extraction and interview evaluation."""

from __future__ import annotations

import re
from typing import Any, Dict, List, Tuple


KNOWN_SKILLS = {
    "python", "sql", "machine learning", "deep learning", "nlp", "computer vision",
    "tensorflow", "pytorch", "scikit-learn", "pandas", "numpy", "statistics",
    "tableau", "powerbi", "excel", "spark", "pyspark", "hadoop", "kafka", "airflow",
    "aws", "azure", "gcp", "docker", "kubernetes", "linux", "terraform", "jenkins",
    "django", "flask", "fastapi", "react", "node", "javascript", "typescript",
    "html", "css", "api", "microservices", "postgresql", "mysql", "mongodb", "redis",
    "git", "ci/cd", "java", "c++", "c#", "go", "rust", "devops",
}

ROLE_KEYWORDS = {
    "data scientist": ["python", "sql", "machine learning", "statistics", "pandas", "model"],
    "machine learning engineer": ["python", "pytorch", "tensorflow", "mlops", "docker", "api"],
    "data analyst": ["sql", "excel", "tableau", "powerbi", "statistics", "dashboard"],
    "backend developer": ["python", "django", "flask", "api", "postgresql", "docker"],
    "devops engineer": ["linux", "docker", "kubernetes", "terraform", "ci/cd", "aws"],
    "full stack developer": ["javascript", "react", "node", "api", "sql", "git"],
}

ROLE_QUESTIONS = {
    "data scientist": "Explain a machine learning project where you improved model performance and validated results.",
    "machine learning engineer": "How would you take a trained ML model to production and monitor it?",
    "data analyst": "Describe how you converted raw data into business insights for decision making.",
    "backend developer": "Design a scalable API for a high-traffic application. What trade-offs would you consider?",
    "devops engineer": "How would you design a CI/CD pipeline with reliable rollback and monitoring?",
    "full stack developer": "Describe how you optimized both frontend and backend performance in one project.",
}

FILLER_WORDS = {"um", "uh", "like", "basically", "actually", "you know", "sort of", "kind of"}
ACTION_VERBS = {
    "built", "implemented", "designed", "optimized", "deployed", "improved", "automated",
    "reduced", "increased", "analyzed", "created", "developed", "led",
}
RESULT_TERMS = {"improved", "increased", "reduced", "faster", "accuracy", "latency", "cost", "%", "percent"}


def _canonical(text: str) -> str:
    return re.sub(r"\s+", " ", str(text or "").strip().lower())


def _find_skills(text: str) -> List[str]:
    hay = _canonical(text)
    found = []
    for skill in sorted(KNOWN_SKILLS, key=len, reverse=True):
        if re.search(r"\b" + re.escape(skill) + r"\b", hay):
            found.append(skill)
    return list(dict.fromkeys(found))


def _extract_years(text: str) -> float:
    hay = _canonical(text)
    m = re.search(r"(\d+(?:\.\d+)?)\s*(?:\+)?\s*(?:years|year|yrs|yr)", hay)
    if not m:
        return 0.0
    try:
        return float(m.group(1))
    except ValueError:
        return 0.0


def _extract_education(text: str) -> str:
    hay = _canonical(text)
    if any(k in hay for k in ["phd", "doctorate"]):
        return "Doctorate"
    if any(k in hay for k in ["mtech", "m.tech", "masters", "master", "msc", "m.s", "post graduate"]):
        return "Masters"
    if any(k in hay for k in ["btech", "b.tech", "bachelor", "bachelors", "bsc", "b.e", "be"]):
        return "Bachelors"
    if any(k in hay for k in ["diploma"]):
        return "Diploma"
    return ""


def _extract_interests(text: str, skills: List[str]) -> List[str]:
    hay = _canonical(text)
    interests: List[str] = []

    patterns = [
        r"interested in ([a-z0-9\s,\-/+#]+)",
        r"want to work in ([a-z0-9\s,\-/+#]+)",
        r"target role is ([a-z0-9\s,\-/+#]+)",
        r"looking for ([a-z0-9\s,\-/+#]+)",
    ]
    for pattern in patterns:
        m = re.search(pattern, hay)
        if m:
            segment = m.group(1)
            parts = [p.strip() for p in re.split(r",|and", segment) if p.strip()]
            for p in parts:
                if len(p) >= 3:
                    interests.append(p)

    role_hints = ["data scientist", "machine learning engineer", "data analyst", "backend developer", "devops engineer", "full stack developer"]
    for role in role_hints:
        if role in hay:
            interests.append(role)

    interests.extend(skills[:3])
    return list(dict.fromkeys(interests))[:8]


def extract_profile_from_transcript(transcript: str) -> Dict[str, Any]:
    text = str(transcript or "").strip()
    if len(text) < 8:
        return {
            "success": False,
            "message": "Transcript is too short. Please speak a little more detail.",
        }

    skills = _find_skills(text)
    years = _extract_years(text)
    education = _extract_education(text)
    interests = _extract_interests(text, skills)

    structured_profile = {
        "skills": skills,
        "interests": interests,
        "education": {"degrees": [education] if education else []},
        "experience": [{"years": years}] if years > 0 else [],
    }

    confidence = 45
    if skills:
        confidence += min(30, len(skills) * 4)
    if years > 0:
        confidence += 10
    if education:
        confidence += 8
    if interests:
        confidence += 7

    return {
        "success": True,
        "structured_profile": structured_profile,
        "entities": {
            "skills": skills,
            "years_experience": years,
            "education": education,
            "interests": interests,
        },
        "confidence": min(100, confidence),
    }


def _resolve_role(role: str) -> Tuple[str, List[str]]:
    role_key = _canonical(role)
    if role_key in ROLE_KEYWORDS:
        return role_key, ROLE_KEYWORDS[role_key]

    for known_role, keywords in ROLE_KEYWORDS.items():
        if known_role in role_key or role_key in known_role:
            return known_role, keywords

    return role_key or "general software role", ["python", "sql", "api", "git"]


def generate_interview_question(role: str) -> Dict[str, Any]:
    role_key, _ = _resolve_role(role)
    question = ROLE_QUESTIONS.get(
        role_key,
        "Describe one challenging project, your approach, and measurable impact.",
    )
    return {
        "success": True,
        "role": role_key,
        "question": question,
    }


def evaluate_interview_answer(role: str, answer: str) -> Dict[str, Any]:
    role_key, target_keywords = _resolve_role(role)
    text = str(answer or "").strip()

    if len(text) < 20:
        return {
            "success": False,
            "message": "Answer is too short. Please provide at least 2-3 detailed sentences.",
        }

    norm = _canonical(text)
    words = re.findall(r"[a-zA-Z0-9+#/.%-]+", norm)
    word_count = len(words)

    coverage_hits = [kw for kw in target_keywords if re.search(r"\b" + re.escape(kw) + r"\b", norm)]
    keyword_score = round((len(coverage_hits) / max(1, len(target_keywords))) * 100)

    sentence_count = max(1, len(re.findall(r"[.!?]", text)))
    structure_score = 55
    if word_count >= 70:
        structure_score += 20
    if sentence_count >= 3:
        structure_score += 15
    if re.search(r"\b(first|then|finally|because|therefore|result)\b", norm):
        structure_score += 10
    structure_score = min(100, structure_score)

    action_hits = sum(1 for verb in ACTION_VERBS if re.search(r"\b" + re.escape(verb) + r"\b", norm))
    result_hits = sum(1 for term in RESULT_TERMS if term in norm)
    impact_score = min(100, 40 + action_hits * 12 + result_hits * 10)

    filler_count = 0
    for filler in FILLER_WORDS:
        filler_count += len(re.findall(r"\b" + re.escape(filler) + r"\b", norm))
    filler_ratio = filler_count / max(1, word_count)
    communication_score = max(30, min(100, int(92 - filler_ratio * 200)))

    overall = round(
        keyword_score * 0.35
        + structure_score * 0.25
        + impact_score * 0.25
        + communication_score * 0.15,
        1,
    )

    strengths: List[str] = []
    improvements: List[str] = []

    if len(coverage_hits) >= max(2, len(target_keywords) // 2):
        strengths.append("Good role-specific technical coverage.")
    else:
        improvements.append("Mention more role-specific concepts and tools.")

    if impact_score >= 70:
        strengths.append("You described concrete actions and outcomes.")
    else:
        improvements.append("Add measurable outcomes (for example: latency reduced by 30%).")

    if structure_score >= 75:
        strengths.append("Answer has clear structure and flow.")
    else:
        improvements.append("Use STAR format: Situation, Task, Action, Result.")

    if communication_score < 65:
        improvements.append("Reduce filler words and keep sentences concise.")

    if not strengths:
        strengths.append("You attempted a complete response for the question.")

    return {
        "success": True,
        "role": role_key,
        "overall_score": overall,
        "rubric": {
            "keyword_coverage": keyword_score,
            "structure": structure_score,
            "impact": impact_score,
            "communication": communication_score,
        },
        "matched_keywords": coverage_hits,
        "strengths": strengths,
        "improvements": improvements[:5],
        "word_count": word_count,
    }
