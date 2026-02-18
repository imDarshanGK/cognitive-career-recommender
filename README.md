# CareerAI - Career Recommendation System

A skill-based career matching platform that helps users find suitable roles based on resume or manual input.

## Features

- Resume upload and parsing (PDF, DOCX)
- Manual profile input mode
- Skill-based career matching against 7 role types
- Explainable recommendations with skill gaps
- Learning roadmap generation
- Feedback tracking
- Secure authentication with bcrypt password hashing
- Security headers and CSRF protection

## Quick Start

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables (optional for development)
cp .env.example .env
# Edit .env file with your settings

# For enhanced NLP features (optional)
python -m spacy download en_core_web_sm
python -m nltk.downloader punkt stopwords

# Run the application
python backend/app.py
```

Visit http://127.0.0.1:5000

Test: admin@example.com / admin123

## Tech Stack

- Flask 3.0.0
- bcrypt (secure password hashing)
- SQLite (feedback storage)
- Bootstrap 5.3
- Vanilla JavaScript
- Optional: scikit-learn, spaCy, NLTK for enhanced features

## Security Features

- Bcrypt password hashing with automatic salting
- Security headers (CSP, X-Frame-Options, etc.)
- CSRF protection for forms and JSON requests
- Input validation for file uploads
- Environment-based configuration

## Configuration

See `.env.example` for available configuration options. Key settings:

- `DEBUG`: Set to `False` in production
- `SECRET_KEY`: Use a strong, random secret key in production
- `FLASK_ENV`: Set to `production` for deployment
## Deployment

Docker: `docker-compose up`  
Or: Render.com, Railway.app, DigitalOcean, AWS

## Development Notes

- The app uses in-memory user storage by default. For production, implement a proper database.
- ML/NLP features are optional and will gracefully degrade if dependencies are not installed.
- Always set `DEBUG=False` and use strong `SECRET_KEY` in production.
