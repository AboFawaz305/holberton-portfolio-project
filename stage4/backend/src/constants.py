"""Global commonly used constants
"""
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
UPLOAD_DIR = BASE_DIR / "uploads"
ORG_PHOTOS_DIR = UPLOAD_DIR / "organizations"
SECRET_KEY = "wow_secret_KEY"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


RESEND_API_KEY = "re_xxxxxxxxxxxx"  # resend API key
FRONTEND_URL = "http://localhost:5173"
FROM_EMAIL = "onboarding@resend.dev"  # domain email