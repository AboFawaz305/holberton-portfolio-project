"""Global commonly used constants
"""
from pathlib import Path

BASE_DIR = Path("/static")
UPLOAD_DIR = BASE_DIR / "uploads"
ORG_PHOTOS_DIR = UPLOAD_DIR / "organizations"
GROUPS_RESOURCES_DIR = UPLOAD_DIR / "groups" / "resources"
SECRET_KEY = "wow_secret_KEY"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60
RESEND_API_KEY = "re_ffffffffffffff"  # resend API key
FRONTEND_URL = "http://localhost:80"
FROM_EMAIL = "Atrab <no-reply@atrab.app>"  # domain email
