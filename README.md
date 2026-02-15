# CareerAI - Career Recommendation System

A skill-based career matching platform that helps users find suitable roles based on resume or manual input.

## Features

- Resume upload and parsing (PDF, DOCX)
- Manual profile input mode
- Skill-based career matching against 7 role types
- Explainable recommendations with skill gaps
- Learning roadmap generation
- Feedback tracking

## Quick Start

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python backend/app.py
```

Visit http://127.0.0.1:5000

Test: admin@example.com / admin123

## Tech Stack

- Flask 3.0.0
- SQLite (feedback storage)
- Bootstrap 5.3
- Vanilla JavaScript

## Deployment

Docker: `docker-compose up`  
Or: Render.com, Railway.app, DigitalOcean, AWS
