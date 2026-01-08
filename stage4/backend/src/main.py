"""Main App definition
"""

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from api.authentication import auth
from api.chat import chat
from api.organizations import orgs
from api.users import users
from constants import ORG_PHOTOS_DIR, UPLOAD_DIR

ORG_PHOTOS_DIR.mkdir(parents=True, exist_ok=True)

load_dotenv("../../.env", verbose=True)


app = FastAPI(root_path="/api")
app.include_router(auth)
app.include_router(orgs)
app.include_router(chat)
app.include_router(users)
app.mount("/static", StaticFiles(directory=UPLOAD_DIR), name="static")
