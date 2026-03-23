"""Application configuration for the CareerAI backend."""

import os
from pathlib import Path

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parent

# Load local env files for dev; keep platform env vars (Render, Docker, etc.) as priority.
load_dotenv(BASE_DIR / ".env", override=False)
load_dotenv(PROJECT_ROOT / ".env", override=False)


def _to_int(value, default):
    """Parse integer env values safely, even when comments are present."""
    if value is None:
        return default
    cleaned = str(value).split("#", 1)[0].strip()
    try:
        return int(cleaned)
    except (TypeError, ValueError):
        return default


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-me")
    DEBUG = os.getenv("DEBUG", "False").lower() in ("1", "true", "t", "yes")

    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL", f"sqlite:///{BASE_DIR / 'instance' / 'career_system.db'}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAX_CONTENT_LENGTH = _to_int(os.getenv("MAX_CONTENT_LENGTH"), 16 * 1024 * 1024)
    UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", str(BASE_DIR / "instance" / "uploads"))
    ALLOWED_EXTENSIONS = {"pdf", "doc", "docx", "txt"}

    MAIL_SERVER = os.getenv("MAIL_SERVER", "smtp.gmail.com")
    MAIL_PORT = _to_int(os.getenv("MAIL_PORT"), 587)
    MAIL_USERNAME = os.getenv("MAIL_USERNAME", "")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD", "")
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER", MAIL_USERNAME or "noreply@careerai.local")

    PERMANENT_SESSION_LIFETIME = _to_int(os.getenv("SESSION_LIFETIME_SECONDS"), 86400)

    @staticmethod
    def init_app(app):
        """Create required runtime directories for local/dev deployments."""
        os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
        db_path = app.config.get("SQLALCHEMY_DATABASE_URI", "")
        if db_path.startswith("sqlite:///"):
            sqlite_file = db_path.replace("sqlite:///", "", 1)
            parent_dir = os.path.dirname(sqlite_file)
            if parent_dir:
                os.makedirs(parent_dir, exist_ok=True)
