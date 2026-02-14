# Cognitive Career Recommender - Complete Specifications

## SECTION 1 — CORE BACKEND GOAL

Your backend must do 5 real things:

1. **Accept user profile** (resume OR manual details)
2. **Extract structured data** (skills, education, experience)
3. **Match against career roles dataset**
4. **Generate explainable reasoning**
5. **Provide learning roadmap**

That's enough for academic Cognitive AI project.

---

## SECTION 2 — USER INPUT OPTIONS (VERY IMPORTANT)

You asked: resume sometimes not available. What to do?

**Correct solution: Provide TWO INPUT MODES.**

- **Resume Upload Mode**
- **Manual Profile Mode**

Both must generate the same structured profile internally.

### A) Resume Upload Flow

User uploads:
- PDF
- DOCX

Backend Process:

**Step 1: Extract text**
- Use: PyPDF2 or pdfplumber (for PDF)
- Use: python-docx (for DOCX)

**Step 2: Clean text**
- Remove: Extra spaces
- Remove: Symbols
- Remove: Headers/footers

**Step 3: NLP Skill Extraction**
- Use: spaCy
- Use: Skill keyword dictionary
- OR simple TF-IDF based matching

Extract:
- Skills
- Degree
- Experience keywords
- Projects keywords

**Step 4: Convert into structured JSON**

Example:
```json
{
  "skills": ["python", "machine learning", "sql"],
  "education": "B.Tech",
  "experience_level": "entry",
  "interests": []
}
```

This becomes user profile.

### B) Manual Input Mode

User fills:
- Education level
- Skills (comma separated)
- Years of experience
- Career interest area

Backend converts directly into structured JSON like above.

**Important:**
Both resume mode and manual mode must end in SAME STRUCTURE.
So your system logic remains clean.

---

## SECTION 3 — CAREER DATABASE (REALISTIC)

You need a career dataset.

Do NOT fake real-time jobs unless you integrate API.

Better approach for academic project: Create structured career dataset.

Example structure:
```json
[
  {
    "role": "Data Scientist",
    "required_skills": ["python", "machine learning", "statistics"],
    "experience_level": "entry",
    "related_skills_to_learn": ["deep learning", "data visualization"]
  },
  {
    "role": "Backend Developer",
    "required_skills": ["python", "django", "sql"],
    "experience_level": "entry",
    "related_skills_to_learn": ["api design", "system design"]
  }
]
```

You can build:
- CSV file
- OR JSON file
- OR SQLite database

This is realistic and manageable.

---

## SECTION 4 — MATCHING ENGINE (CORE AI PART)

Now real Cognitive AI logic.

**Basic matching algorithm:**

1. Convert user skills to lowercase
2. Compare with required_skills
3. Calculate match score:

```
Match Score = (number of matched skills / total required skills) * 100
```

This is simple and real.

**Optional advanced:**
- TF-IDF vectorization
- Cosine similarity
- Sentence transformers (if you want advanced)

But basic matching is enough for project.

---

## SECTION 5 — EXPLAINABLE AI LOGIC (VERY IMPORTANT)

This is your strongest part.

For each recommendation: **Explain WHY.**

Example logic:
- If user skill matches required skill → Add explanation line
- If user missing skill → Add gap explanation

**Example output:**

```
Top Match: Data Scientist
Score: 75%

Explanation:
• Your Python skill matches required skill.
• Your Machine Learning background aligns with role.
• Missing: Deep Learning and Data Visualization.
```

This is real XAI. No fake reasoning.

---

## SECTION 6 — LEARNING ROADMAP GENERATOR

Based on missing skills: Create roadmap automatically.

**Example logic:**

Missing skills = required_skills - user_skills

For each missing skill: Add to roadmap list.

**Output:**

```
Roadmap:

Learn Deep Learning
Practice Data Visualization
Build 2 ML projects
```

You can even map each skill to:
- Beginner resource
- Intermediate project suggestion

Keep simple.

---

## SECTION 7 — REAL-TIME JOB OPTION (IF YOU WANT)

If you want real jobs:

**Option 1:**
- Use public APIs like: Adzuna API, RapidAPI job search

**Option 2:**
- Scrape (not recommended for project)

**Important:**
If you do NOT integrate API, do NOT claim real-time jobs.

Safer approach:
Use static dataset and call it: **"Career Role Recommendations"**

Not "Live Jobs".

---

## SECTION 8 — DATABASE DESIGN

Use:
- SQLite (simple)
- OR PostgreSQL (if advanced)

**Tables:**

#### Users
- id
- name
- email
- password_hash
- created_at

#### Profiles
- user_id
- skills (JSON)
- education
- experience_level

#### Recommendations
- user_id
- role
- score
- generated_at

#### Feedback
- user_id
- role
- liked (true/false)

---

## SECTION 9 — FEEDBACK LOOP (Cognitive AI Feature)

If user clicks:
- 👍 Relevant
- 👎 Not relevant

Store feedback.

**Future improvement:**
- Increase score weight for liked roles.
- Decrease for disliked.

That becomes **Adaptive Learning**.

---

## SECTION 10 — BACKEND STACK

Recommended stack:
- Python
- FastAPI (better than Flask)
- SQLite
- spaCy
- scikit-learn
- Pydantic

**Why FastAPI?**
- Clean API
- Automatic docs
- Good for AI projects

---

## SECTION 11 — DASHBOARD AFTER LOGIN

When user logs in, show:

### Sidebar Menu:
- Dashboard
- My Profile
- Upload Resume
- Career Matches
- Skill Gap
- Learning Roadmap
- Feedback History
- Logout

### Dashboard Layout:

**Top Section:**
- User name
- Profile completion %

**Middle Section:**
- Top 3 Career Matches (cards)
- Each card: Role, Match Score, View Explanation button

**Bottom Section:**
- Skill Gap Summary
- Roadmap Preview

---

## SECTION 12 — COLOR SYSTEM (Professional AI Look)

Use 3 primary colors only:

- **Primary:** Indigo / Deep Blue
- **Secondary:** Teal
- **Accent:** Amber

**Background:** Light gray (#f5f7fa)

**Cards:** White

**Buttons:** Primary gradient (Indigo → Blue)

**Avoid:**
- Too many colors
- Red/Green heavy usage

---

## SECTION 13 — WHAT NOT TO DO

Do NOT:
- Claim real-time jobs without API
- Show fake growth percentages
- Add fake user count
- Add fake salary prediction
- Use random numbers

**Everything must be calculated from your logic.**

---

## FINAL CLEAN SYSTEM FLOW

```
User Register
→ Upload Resume OR Manual Fill
→ NLP Extraction
→ Structured Profile
→ Career Matching Engine
→ Match Score Calculation
→ Explainable AI Output
→ Skill Gap
→ Learning Roadmap
→ Feedback
→ Stored in DB
```

---

## HOW TO RUN

```bash
cd backend
python simple_app.py
```

Access at `http://localhost:5000`

---

## QUICK START TEST

1. Register with your name, email, password
2. Login
3. Go to **My Profile** - See your actual name (not "Darshan")
4. Upload resume or enter skills manually
5. Go to **Career Matches** - See recommendations with explanations
6. Check **Learning Roadmap** - See personalized skill paths
