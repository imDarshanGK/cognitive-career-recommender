# Cognitive Career & Job Recommendation System with Explainable and Adaptive AI

## Overview

This project implements an advanced AI-based career and job recommendation system that uses cognitive reasoning, explainable AI, and adaptive learning to provide personalized career guidance. The system analyzes user profiles through NLP-based resume processing and generates intelligent recommendations with clear explanations.

## Problem Statement

In today's competitive job market, students and job seekers face difficulty in choosing suitable careers and jobs because their skills, interests, and qualifications often do not match available opportunities. Traditional job recommendation systems provide suggestions but do not explain why a particular job is recommended and lack contextual understanding and reasoning ability.

## Objectives

- Analyze user profile (skills, interests, education, experience)
- Extract information from resumes using NLP (Natural Language Processing)
- Analyze user behavior and preferences
- Build a machine learning model for job recommendation
- Create a cognitive reasoning layer to justify recommendations
- Provide explainable AI-based job suggestions
- Learn and improve recommendations using user feedback

## Methodology / Workflow (Cognitive AI Flow)

1. **User Input Collection** (skills, interests, resume data)
2. **Data Preprocessing & Feature Extraction**
3. **NLP-based Skill & Interest Analysis**
4. **Machine Learning Model for Job Matching**
5. **Cognitive Reasoning Layer** (Why this job is recommended?)
6. **Explainable AI Output**
7. **Feedback-based Learning**

### Cognitive Loop
**Observe → Understand → Analyze → Reason → Decide → Explain → Learn**

## Tech Stack

- **Programming Language**: Python
- **AI/ML Libraries**: Scikit-learn, TensorFlow, Pandas, NumPy
- **Cognitive AI / Explainable AI**: SHAP, LIME
- **NLP Libraries**: spaCy, NLTK, TextBlob
- **Frontend**: Flask with Bootstrap
- **Data**: Kaggle Job Dataset, Custom Resume Dataset

## Project Structure

```
cognitive-career-recommender/
├── backend/
│   ├── app.py                          # Main Flask application
│   ├── config.py                       # Configuration settings
│   ├── requirements.txt                # Python dependencies
│   ├── ai_engine/
│   │   └── cognitive_engine.py         # Core cognitive AI engine
│   ├── nlp_processor/
│   │   └── resume_analyzer.py          # NLP resume analysis
│   ├── utils/
│   │   └── data_processor.py           # Data processing utilities
│   ├── models/                         # Trained ML models
│   ├── data/                           # Datasets and uploads
│   ├── templates/                      # Flask templates
│   └── static/                         # Static assets
└── README.md                           # Project documentation
```

## Installation and Setup

### Prerequisites
- Python 3.8 or higher

### Step 1: Navigate to Backend Directory
```bash
cd cognitive-career-recommender/backend
```

### Step 2: Create Virtual Environment
```bash
python -m venv career_ai_env
career_ai_env\Scripts\activate  # On Windows
# source career_ai_env/bin/activate  # On Linux/Mac
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Download NLP Models
```bash
python -m spacy download en_core_web_sm
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"
```

### Step 5: Run the Application
```bash
python simple_app.py
```

Access the application at `http://localhost:5000`
- **Dashboard**: `http://localhost:5000/dashboard`
- **API Test**: `http://localhost:5000/api/test`

## Built by Team AKATSUKI