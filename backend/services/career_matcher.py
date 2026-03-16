"""Real-time skill-based career matcher using live job data."""

from __future__ import annotations

import re
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Dict, List, Set

from utils.data_processor import DataProcessor


SKILL_ALIASES = {
    "rest api": "api",
    "rest apis": "api",
    "apis": "api",
    "ml": "machine learning",
    "artificial intelligence": "ai",
    "data analytics": "data analysis",
    "power bi": "powerbi",
    "node.js": "node",
    "js": "javascript",
    "py": "python",
    "structured query language": "sql",
    "ci cd": "ci/cd",
    "cloud": "cloud platforms",
    "sklearn": "scikit-learn",
    "dl": "deep learning",
    "cv": "computer vision",
    "pgsql": "postgresql",
    "postgres": "postgresql",
}

# Vocabulary for extracting market-demand skills from job text.
KNOWN_SKILLS = {
    # Core languages
    "python", "java", "javascript", "typescript", "c++", "c#", "go", "rust",
    "scala", "kotlin", "r", "matlab",
    # Data / ML / AI
    "sql", "data analysis", "machine learning", "deep learning", "nlp",
    "computer vision", "tensorflow", "pytorch", "scikit-learn",
    "pandas", "numpy", "statistics", "excel", "tableau", "powerbi",
    "transformers", "huggingface",
    # Big data
    "spark", "pyspark", "hadoop", "hive", "kafka", "airflow", "hbase",
    # Cloud
    "aws", "azure", "gcp", "cloud platforms",
    # DevOps / infra
    "docker", "kubernetes", "terraform", "ansible", "jenkins", "linux",
    "ci/cd", "git", "devops",
    # Web / backend
    "django", "flask", "fastapi", "spring", "spring boot", "node",
    "react", "angular", "vue", "html", "css",
    "api", "graphql", "grpc", "microservices", "websocket", "rest",
    # Databases
    "postgresql", "mysql", "mongodb", "redis", "elasticsearch", "sqlite",
    # Testing / QA
    "pytest", "selenium", "unittest", "automation", "testing",
    # Other tools
    "celery", "scrapy", "beautifulsoup",
    "agile", "scrum", "jira",
}


def _canonical_skill(skill: str) -> str:
    text = re.sub(r"\s+", " ", str(skill or "").strip().lower())
    text = text.replace("-", " ")
    return SKILL_ALIASES.get(text, text)


def _tokenize_skills(raw_skills: Any) -> List[str]:
    if not raw_skills:
        return []

    if isinstance(raw_skills, str):
        candidates = raw_skills.split(",")
    elif isinstance(raw_skills, list):
        candidates = raw_skills
    else:
        return []

    normalized = []
    for item in candidates:
        text = _canonical_skill(item)
        if text:
            normalized.append(text)

    return list(dict.fromkeys(normalized))


def _normalize_profile(user_data: Dict[str, Any]) -> Dict[str, Any]:
    skills = _tokenize_skills(user_data.get("skills", []))

    interests_raw = user_data.get("interests", [])
    if isinstance(interests_raw, str):
        interests = _tokenize_skills(interests_raw)
    elif isinstance(interests_raw, list):
        interests = _tokenize_skills(interests_raw)
    else:
        interests = []

    experience = user_data.get("experience", []) or []
    years = 0.0
    if isinstance(experience, list):
        for entry in experience:
            try:
                years += float(entry.get("years", 0))
            except (TypeError, ValueError, AttributeError):
                continue

    return {
        "skills": skills,
        "skills_set": set(skills),
        "interests": interests,
        "experience_years": years,
        "education": user_data.get("education", {}) or {},
    }


def _extract_job_skills(job: Dict[str, Any]) -> List[str]:
    blob = " ".join([
        str(job.get("job_title", "")),
        str(job.get("description", "")),
    ]).lower()

    found = []
    for skill in sorted(KNOWN_SKILLS, key=len, reverse=True):
        pattern = r"\b" + re.escape(skill) + r"\b"
        if re.search(pattern, blob):
            found.append(_canonical_skill(skill))

    return list(dict.fromkeys(found))


def _score_job(user_skills: Set[str], required_skills: List[str]) -> Dict[str, Any]:
    required = _tokenize_skills(required_skills)
    if not required:
        return {"match_score": 0.0, "matched_skills": [], "missing_skills": []}

    matched = [s for s in required if s in user_skills]
    missing = [s for s in required if s not in user_skills]
    score = round((len(matched) / len(required)) * 100, 2)

    return {
        "match_score": score,
        "matched_skills": matched,
        "missing_skills": missing,
    }


def _build_query(skills: List[str], interests: List[str]) -> str:
    primary = skills[:3]
    if primary:
        return " ".join(primary)
    if interests:
        return " ".join(interests[:2])
    return "software"


def _infer_work_type(employment_type: str, location: str, description: str) -> str:
    text = " ".join([str(employment_type or ""), str(location or ""), str(description or "")]).lower()
    if "hybrid" in text:
        return "hybrid"
    if "remote" in text or "work from home" in text or "wfh" in text:
        return "remote"
    if text:
        return "onsite"
    return ""


def _infer_industry(job_title: str, description: str) -> str:
    text = " ".join([str(job_title or ""), str(description or "")]).lower()
    if any(k in text for k in ["fintech", "bank", "payments"]):
        return "fintech"
    if any(k in text for k in ["health", "healthcare", "medical", "hospital"]):
        return "healthcare"
    if any(k in text for k in ["ecommerce", "e-commerce", "retail"]):
        return "ecommerce"
    if any(k in text for k in ["consulting", "consultant", "advisory"]):
        return "consulting"
    return "technology"


def _build_skill_gap(top_jobs: List[Dict[str, Any]], user_skills: Set[str], max_items: int = 8) -> List[str]:
    missing_counter: Counter[str] = Counter()

    for job in top_jobs:
        for skill in job.get("missing_skills", []):
            canonical = _canonical_skill(skill)
            if canonical and canonical not in user_skills:
                missing_counter[canonical] += 1

    return [skill for skill, _ in missing_counter.most_common(max_items)]


def _skill_specific_steps(skill: str) -> List[str]:
    normalized = _canonical_skill(skill)
    templates = {
        "django": [
            "Learn Django models, views, and REST framework basics",
            "Build a blog or task-manager API project",
            "Deploy on Render or AWS with environment variables",
            "Publish code, docs, and API examples on GitHub",
        ],
        "tensorflow": [
            "Learn TensorFlow tensors, datasets, and training loops",
            "Build an image classifier end-to-end",
            "Serve the model through a small inference API",
            "Deploy and track model performance metrics",
        ],
        "docker": [
            "Learn Docker images, containers, and networking",
            "Containerize your app and database",
            "Use Docker Compose for local orchestration",
            "Deploy containerized app to cloud runtime",
        ],
        "aws": [
            "Learn core AWS services (EC2, S3, RDS)",
            "Deploy one project with IAM and environment secrets",
            "Set up monitoring and budget alerts",
            "Document architecture and deployment steps",
        ],
        "api": [
            "Learn REST design and HTTP status codes",
            "Build CRUD endpoints with validation",
            "Add authentication and request throttling",
            "Document APIs using OpenAPI/Postman",
        ],
    }

    return templates.get(
        normalized,
        [
            f"Learn {skill} fundamentals",
            f"Build one practical project using {skill}",
            f"Deploy the project with tests",
            f"Publish implementation and notes on GitHub",
        ],
    )


def build_roadmap(missing_skills: List[str], max_items: int = 6) -> List[Dict[str, Any]]:
    roadmap = []
    for idx, skill in enumerate(missing_skills[:max_items], 1):
        roadmap.append(
            {
                "skill": skill,
                "phase": f"Step {idx}: {skill.title()}",
                "actions": _skill_specific_steps(skill),
                "estimated_time": "2-4 weeks",
            }
        )
    return roadmap


def _estimate_confidence(required: List[str], matched: List[str], demand_count: int, source: str = "adzuna") -> Dict[str, Any]:
    required_count = max(1, len(required))
    overlap_ratio = len(matched) / required_count
    demand_score = min(1.0, float(max(0, demand_count)) / 8.0)
    source_bonus = 0.1 if source == "adzuna" else 0.0

    confidence = round((overlap_ratio * 0.65 + demand_score * 0.25 + source_bonus) * 100, 1)
    confidence = max(20.0, min(95.0, confidence))

    if confidence >= 75:
        band = "high"
    elif confidence >= 50:
        band = "medium"
    else:
        band = "low"

    margin = 8 if band == "high" else (12 if band == "medium" else 16)
    lower = max(0.0, round(confidence - margin, 1))
    upper = min(100.0, round(confidence + margin, 1))

    return {
        "score": confidence,
        "band": band,
        "range": [lower, upper],
    }


def _build_counterfactual(required: List[str], matched: List[str], base_score: float, max_suggestions: int = 2) -> Dict[str, Any]:
    missing = [skill for skill in required if skill not in matched]
    if not missing:
        return {
            "suggested_skills": [],
            "estimated_score": round(float(base_score), 1),
            "estimated_gain": 0.0,
            "message": "You already cover the key skills for this role.",
        }

    suggested = missing[:max_suggestions]
    gain_per_skill = 100.0 / max(1, len(required))
    estimated_gain = round(min(35.0, gain_per_skill * len(suggested) * 0.9), 1)
    estimated_score = round(min(100.0, float(base_score) + estimated_gain), 1)

    return {
        "suggested_skills": suggested,
        "estimated_score": estimated_score,
        "estimated_gain": estimated_gain,
        "message": f"Learning {', '.join(suggested)} can raise this match by about +{estimated_gain}%.",
    }


def _aggregate_careers(matched_jobs: List[Dict[str, Any]], interests: List[str], user_skills: Set[str] = None) -> List[Dict[str, Any]]:
    by_title: Dict[str, Dict[str, Any]] = defaultdict(lambda: {
        "required_counter": Counter(),
        "matched_counter": Counter(),
        "location_counter": Counter(),
        "work_type_counter": Counter(),
        "industry_counter": Counter(),
        "salary_min_values": [],
        "salary_max_values": [],
        "samples": 0,
    })

    for job in matched_jobs:
        title = str(job.get("job_title", "")).strip() or "Career Role"
        bucket = by_title[title]
        bucket["samples"] += 1

        for s in job.get("required_skills", []):
            bucket["required_counter"][_canonical_skill(s)] += 1
        for s in job.get("matched_skills", []):
            bucket["matched_counter"][_canonical_skill(s)] += 1

        location = str(job.get("location", "")).strip()
        if location:
            bucket["location_counter"][location] += 1

        work_type = _infer_work_type(job.get("employment_type", ""), job.get("location", ""), job.get("description", ""))
        if work_type:
            bucket["work_type_counter"][work_type] += 1

        industry = _infer_industry(job.get("job_title", ""), job.get("description", ""))
        if industry:
            bucket["industry_counter"][industry] += 1

        salary_min = job.get("salary_min")
        salary_max = job.get("salary_max")
        if isinstance(salary_min, (int, float)) and salary_min > 0:
            bucket["salary_min_values"].append(float(salary_min))
        if isinstance(salary_max, (int, float)) and salary_max > 0:
            bucket["salary_max_values"].append(float(salary_max))

    careers = []
    for title, bucket in by_title.items():
        required = [s for s, _ in bucket["required_counter"].most_common(8)]
        matched = [s for s, _ in bucket["matched_counter"].most_common(8)]
        missing = [s for s in required if s not in matched]

        if not required:
            continue

        score = round((len(matched) / len(required)) * 100, 2)

        # Title-match bonus: reward roles where the user's skills appear
        # directly in the job title (signals a role centred on that skill).
        title_lower = title.lower()
        if user_skills:
            title_hits = sum(
                1 for s in user_skills
                if len(s) > 2 and re.search(r"\b" + re.escape(s) + r"\b", title_lower)
            )
        else:
            title_hits = 0
        title_bonus = min(15.0, float(title_hits) * 7.0)

        # Description-depth bonus: more matched skills from the user = higher confidence.
        depth_bonus = min(10.0, float(len(matched)) * 3.0) if len(matched) > 1 else 0.0

        final_score = min(100.0, round(score + title_bonus + depth_bonus, 2))
        confidence = _estimate_confidence(required, matched, bucket["samples"], source="adzuna")
        counterfactual = _build_counterfactual(required, matched, final_score)

        interest_hits = sum(1 for i in interests if _canonical_skill(i) in title_lower)
        dominant_location = bucket["location_counter"].most_common(1)[0][0] if bucket["location_counter"] else ""
        dominant_work_type = bucket["work_type_counter"].most_common(1)[0][0] if bucket["work_type_counter"] else ""
        dominant_industry = bucket["industry_counter"].most_common(1)[0][0] if bucket["industry_counter"] else "technology"
        salary_min = int(sum(bucket["salary_min_values"]) / len(bucket["salary_min_values"])) if bucket["salary_min_values"] else None
        salary_max = int(sum(bucket["salary_max_values"]) / len(bucket["salary_max_values"])) if bucket["salary_max_values"] else None

        explanation = [
            f"Matched {len(matched)} of {len(required)} core skills from live jobs.",
            f"Based on {bucket['samples']} current job postings.",
            f"Confidence: {confidence['band'].title()} ({confidence['range'][0]}% - {confidence['range'][1]}%).",
        ]
        if title_bonus > 0:
            explanation.append(f"Your skills appear directly in the role title (+{int(title_bonus)} relevance boost).")
        explanation.append(counterfactual["message"])

        careers.append(
            {
                "job_title": title,
                "required_skills": required,
                "matched_skills": matched,
                "missing_skills": missing,
                "match_score": final_score,
                "experience_level": "entry",
                "location": dominant_location,
                "work_type": dominant_work_type,
                "industry": dominant_industry,
                "salary_min": salary_min,
                "salary_max": salary_max,
                "demand_count": bucket["samples"],
                "interest_hits": interest_hits,
                "confidence": confidence["score"],
                "confidence_band": confidence["band"],
                "confidence_range": confidence["range"],
                "counterfactual": counterfactual,
                "explanation": explanation,
            }
        )

    careers.sort(
        key=lambda c: (c["match_score"], c["interest_hits"], c["demand_count"]),
        reverse=True,
    )
    return careers[:10]


def _extract_market_skills(live_jobs: List[Dict[str, Any]]) -> Dict[str, int]:
    counter: Counter[str] = Counter()
    for job in live_jobs:
        for skill in _extract_job_skills(job):
            counter[skill] += 1
    return dict(counter.most_common(12))


def _load_role_catalog() -> List[Dict[str, Any]]:
    catalog_path = Path(__file__).resolve().parents[1] / "data" / "career_roles.json"
    try:
        with catalog_path.open("r", encoding="utf-8") as f:
            payload = json.load(f)
        return payload if isinstance(payload, list) else []
    except Exception:
        return []


def _role_interest_hits(role_title: str, interests: List[str]) -> int:
    title = str(role_title or "").lower()
    if not title:
        return 0

    hits = 0
    for interest in interests:
        canonical = _canonical_skill(interest)
        if not canonical:
            continue

        keywords = {canonical}
        if canonical in {"ai", "machine learning"}:
            keywords.update({"ai", "artificial intelligence", "machine learning", "ml", "data scientist"})
        if canonical in {"data analysis", "data science"}:
            keywords.update({"data", "analyst", "scientist", "analytics"})
        if canonical in {"backend", "backend development"}:
            keywords.update({"backend", "api", "server"})
        if canonical in {"frontend", "frontend development"}:
            keywords.update({"frontend", "ui", "react", "web"})

        if any(keyword in title for keyword in keywords):
            hits += 1

    return hits


def _fallback_catalog_match(profile: Dict[str, Any]) -> Dict[str, Any]:
    catalog = _load_role_catalog()
    if not catalog:
        return {
            "recommendations": [],
            "skill_gap": [],
            "roadmap": [],
            "market_skills": {},
            "live_jobs": [],
            "data_source": "unavailable",
            "data_message": "Live job data and local catalog are unavailable right now.",
        }

    recommendations: List[Dict[str, Any]] = []
    skill_counter: Counter[str] = Counter()

    for role in catalog:
        role_title = role.get("role", "Career Role")
        required = _tokenize_skills(role.get("required_skills", []))
        if not required:
            continue

        scored = _score_job(profile["skills_set"], required)
        if not scored["matched_skills"]:
            continue

        interest_hits = _role_interest_hits(role_title, profile["interests"])
        interest_bonus = min(15.0, float(interest_hits * 8))
        calibrated_score = min(100.0, float(scored["match_score"]) + interest_bonus)
        confidence = _estimate_confidence(required, scored["matched_skills"], demand_count=1, source="local_catalog")
        counterfactual = _build_counterfactual(required, scored["matched_skills"], calibrated_score)

        for skill in required:
            skill_counter[_canonical_skill(skill)] += 1

        explanation = [
            f"Matched {len(scored['matched_skills'])} of {len(required)} required skills from local role catalog.",
            f"Confidence: {confidence['band'].title()} ({confidence['range'][0]}% - {confidence['range'][1]}%).",
        ]
        if interest_bonus > 0:
            explanation.append(f"Interest alignment contributed +{int(interest_bonus)} score.")
        explanation.append(counterfactual["message"])

        recommendations.append(
            {
                "job_title": role_title,
                "required_skills": required,
                "matched_skills": scored["matched_skills"],
                "missing_skills": scored["missing_skills"],
                "match_score": calibrated_score,
                "experience_level": role.get("experience_level", "entry"),
                "location": "",
                "work_type": "",
                "industry": "technology",
                "salary_min": None,
                "salary_max": None,
                "demand_count": 1,
                "interest_hits": interest_hits,
                "confidence": confidence["score"],
                "confidence_band": confidence["band"],
                "confidence_range": confidence["range"],
                "counterfactual": counterfactual,
                "explanation": explanation,
            }
        )

    recommendations.sort(
        key=lambda r: (r["match_score"], r.get("interest_hits", 0), len(r.get("matched_skills", []))),
        reverse=True,
    )
    recommendations = recommendations[:10]

    gap_limit = 5 if len(profile["skills"]) <= 1 else 8
    roadmap_limit = 4 if len(profile["skills"]) <= 1 else 6
    skill_gap = _build_skill_gap(recommendations, profile["skills_set"], max_items=gap_limit)
    roadmap = build_roadmap(skill_gap, max_items=roadmap_limit)

    message = "Live job data unavailable. Showing recommendations from local role catalog."
    if len(profile["skills"]) <= 1 and recommendations:
        message += " Add 2-3 more skills for stronger matches."

    return {
        "recommendations": recommendations,
        "skill_gap": skill_gap,
        "roadmap": roadmap,
        "market_skills": dict(skill_counter.most_common(12)),
        "live_jobs": [],
        "data_source": "local_catalog",
        "data_message": message,
    }


def match_roles(user_data: Dict[str, Any]) -> Dict[str, Any]:
    """Real-time matching pipeline based on live jobs and skill overlap."""
    profile = _normalize_profile(user_data or {})

    if not profile["skills"]:
        return {
            "recommendations": [],
            "normalized_profile": {
                "skills": profile["skills"],
                "interests": profile["interests"],
                "experience_years": profile["experience_years"],
                "experience_level": "entry",
                "education": profile["education"],
            },
            "skill_gap": [],
            "roadmap": [],
            "market_skills": {},
            "live_jobs": [],
            "data_source": "none",
            "data_message": "Add skills to start matching.",
        }

    processor = DataProcessor()
    query = _build_query(profile["skills"], profile["interests"])
    market = processor.get_job_market_data({"query": query, "location": "India", "results": 30})

    live_jobs = market.get("live_jobs", []) if isinstance(market, dict) else []
    source = market.get("source", "unavailable") if isinstance(market, dict) else "unavailable"

    if source != "adzuna" or not live_jobs:
        fallback = _fallback_catalog_match(profile)
        return {
            "recommendations": fallback["recommendations"],
            "normalized_profile": {
                "skills": profile["skills"],
                "interests": profile["interests"],
                "experience_years": profile["experience_years"],
                "experience_level": "entry",
                "education": profile["education"],
            },
            "skill_gap": fallback["skill_gap"],
            "roadmap": fallback["roadmap"],
            "market_skills": fallback["market_skills"],
            "live_jobs": fallback["live_jobs"],
            "data_source": fallback["data_source"],
            "data_message": fallback["data_message"],
        }

    scored_jobs: List[Dict[str, Any]] = []
    for job in live_jobs:
        required = _extract_job_skills(job)
        # Skip low-signal jobs with too few detectable skills.
        if len(required) < 2:
            continue

        scored = _score_job(profile["skills_set"], required)
        overlap_count = len(scored["matched_skills"])
        score = float(scored["match_score"])

        # Keep only jobs with at least one concrete overlap for initial candidate pool.
        if overlap_count < 1 or score <= 0:
            continue

        scored_jobs.append(
            {
                "job_title": job.get("job_title", "Job Role"),
                "company": job.get("company", ""),
                "location": job.get("location", ""),
                "salary_min": job.get("salary_min"),
                "salary_max": job.get("salary_max"),
                "employment_type": job.get("employment_type", ""),
                "redirect_url": job.get("redirect_url", ""),
                "description": job.get("description", ""),
                "required_skills": required,
                "matched_skills": scored["matched_skills"],
                "missing_skills": scored["missing_skills"],
                "match_score": score,
            }
        )

    scored_jobs.sort(key=lambda j: (j["match_score"], len(j.get("matched_skills", []))), reverse=True)

    user_skill_count = len(profile["skills"])
    min_overlap = 2 if user_skill_count >= 2 else 1
    min_score = 25 if user_skill_count >= 2 else 15

    strong_jobs = [
        j for j in scored_jobs
        if len(j.get("matched_skills", [])) >= min_overlap and float(j.get("match_score", 0)) >= min_score
    ]

    # If strict filtering yields nothing, surface low-confidence real overlaps instead of blank results.
    top_jobs = (strong_jobs if strong_jobs else scored_jobs)[:10]

    sparse_profile = user_skill_count <= 1
    if sparse_profile:
        top_jobs = top_jobs[:4]

    careers = _aggregate_careers(top_jobs, profile["interests"], profile["skills_set"])
    if sparse_profile:
        careers = careers[:3]

    gap_limit = 5 if sparse_profile else 8
    roadmap_limit = 4 if sparse_profile else 6
    skill_gap = _build_skill_gap(top_jobs, profile["skills_set"], max_items=gap_limit)
    roadmap = build_roadmap(skill_gap, max_items=roadmap_limit)
    market_skills = _extract_market_skills(live_jobs)

    data_message = ""
    if sparse_profile and top_jobs:
        data_message = "Limited profile detected (1 extracted skill). Showing a small set of low-confidence matches. Add 2-3 more skills for better accuracy."
    elif not strong_jobs and top_jobs:
        data_message = "Limited overlap found. Showing low-confidence matches based on currently extracted skills."

    return {
        "recommendations": careers,
        "normalized_profile": {
            "skills": profile["skills"],
            "interests": profile["interests"],
            "experience_years": profile["experience_years"],
            "experience_level": "entry",
            "education": profile["education"],
        },
        "skill_gap": skill_gap,
        "roadmap": roadmap,
        "market_skills": market_skills,
        "live_jobs": top_jobs,
        "data_source": "adzuna",
        "data_message": data_message,
    }
