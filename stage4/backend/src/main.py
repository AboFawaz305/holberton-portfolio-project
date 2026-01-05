"""API router definitions of the backend
"""

from datetime import datetime, timedelta, timezone
from os import environ as env
from typing import Annotated, List


import shutil
from pathlib import Path
import jwt
from bson.objectid import ObjectId
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, Form
from fastapi.staticfiles import StaticFiles
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import ExpiredSignatureError, PyJWTError
from pwdlib import PasswordHash
from pymongo import MongoClient

from core import NewUser, User, NewOrganizationForm, Organization

load_dotenv("../../.env", verbose=True)

SECRET_KEY = "wow_secret_KEY"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

BASE_DIR = Path(__file__).resolve().parent
UPLOAD_DIR = BASE_DIR / "uploads"
ORG_PHOTOS_DIR = UPLOAD_DIR / "organizations"
ORG_PHOTOS_DIR.mkdir(parents=True, exist_ok=True)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    """token check"""

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except ExpiredSignatureError as es:
        raise HTTPException(status_code=401, detail="token expired") from es
    except PyJWTError as je:
        raise HTTPException(status_code=401, detail="invalid token") from je

    user_id = payload.get("user_id")
    if not user_id:
        raise HTTPException(status_code=401, detail="token missing user_id")

    try:
        object_id = ObjectId(user_id)
    except Exception as ex:
        raise HTTPException(
            status_code=401, detail="invalid user_id format"
            ) from ex

    db = get_engine_db()
    found = db.users.find_one({"_id": object_id})
    if not found:
        raise HTTPException(status_code=401, detail="user not in Database")

    return found


AuthUser = Annotated[User, Depends(get_current_user)]


def get_db_connectoin(host=env.get("MONGO_DB_HOST", "localhost")):
    """Connect to the database"""

    return MongoClient(host, 27017)


def get_engine_db():
    """Get an instance from the main database for the backend"""
    return get_db_connectoin().engine


app = FastAPI(root_path="/api")
password_hash = PasswordHash.recommended()
app.mount("/static", StaticFiles(directory=UPLOAD_DIR), name="static")


@app.post("/register", tags=["User"])
def register_endpoint(user: NewUser):
    """Registeration endpoint to create a new user"""
    db = get_engine_db()
    is_found = db.users.find_one(
        {"$or": [{"username": {"$eq": user.username}},
                 {"email": {"$eq": user.email}}
                 ]}
    )
    if is_found:
        raise HTTPException(status_code=422, detail="User Already Exists.")
    current_time = datetime.now(timezone.utc)
    db.users.insert_one(
        {
            "username": user.username,
            "email": [user.email],
            "password": password_hash.hash(user.password),
            "first_name": user.first_name,
            "last_name": user.last_name,
            "_created_at": current_time,
            "_updated_at": current_time,
        }
    )


@app.post("/login", tags=["User"])
def login_endpoint(
    user: Annotated[OAuth2PasswordRequestForm, Depends()],
):
    """Login endpoint"""

    db = get_engine_db()

    found = db.users.find_one({"username": user.username})
    if not found:
        raise HTTPException(status_code=401, detail="invalid username")
    if not password_hash.verify(user.password, found["password"]):
        raise HTTPException(status_code=401, detail="invalid password")

    exp_time = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )
    token = jwt.encode(
        {"user_id": str(found["_id"]), "exp": exp_time},
        SECRET_KEY, algorithm=ALGORITHM
    )
    return {"access_token": token, "token_type": "bearer"}


@app.get("/me", tags=["User"])
def me_endpoint(user: AuthUser) -> User:
    """route to return user info"""
    return {
        "user_id": str(user["_id"]),
        "first_name": user["first_name"],
        "last_name": user["last_name"],
        "username": user["username"],
        "email": user["email"],
        "created_at": user["_created_at"],
        "updated_at": user["_updated_at"],
    }


@app.post("/organizations", tags=["Organizations"])
async def create_education_organization(
    form: Annotated[NewOrganizationForm, Form()]
):
    """route to create new Organization"""

    db = get_engine_db()
    is_found = db.organizations.find_one(
        {"organization_name": form.organization_name}
        )
    if is_found:
        raise HTTPException(
            status_code=422, detail="Organization already added"
            )

    photo_url = None
    if form.photo and form.photo == "":

        if form.photo.content_type not in ["image/jpeg", "image/png",
                                           "image/gif"]:
            raise HTTPException(
                status_code=400,
                detail="Only JPEG, PNG, and GIF images are allowed."
            )

        file_extension = Path(form.photo.filename).suffix
        unique_name = f"{int(datetime.now(timezone.utc)
                             .timestamp())}{file_extension}"
        file_path = ORG_PHOTOS_DIR / unique_name

        with file_path.open("wb") as buffer:
            shutil.copyfileobj(form.photo.file, buffer)

        photo_url = f"/api/static/organizations/{unique_name}"
    else:
        photo_url = "/api/static/organizations/RR.gif"

    current_time = datetime.now(timezone.utc)
    org_id = db.organizations.insert_one(
        {
            "organization_name": form.organization_name,
            "email_domain": form.email_domain,
            "location": form.location,
            "photo_url": photo_url,
            "users": [],
            "_banned_users": [],
            "_created_at": current_time,
            "_updated_at": current_time,
        }
    )
    return {"message": "Organization added successfully",
            "organization_id": str(org_id.inserted_id)}


@app.get("/organizations", tags=["Organizations"])
def get_all_organization() -> List[Organization]:
    """route to get all Organizations"""

    db = get_engine_db()
    orgs_data = db.organizations.find()

    orgs_list = []
    for org in orgs_data:
        user_count = len(org["users"])
        orgs_list.append(
            {
                "organization_id": str(org["_id"]),
                "organization_name": org["organization_name"],
                "email_domain": org["email_domain"],
                "location": org["location"],
                "photo_url": org["photo_url"],
                "users": org["users"],
                "user_count": user_count,
            }
        )

    return orgs_list


@app.get("/organizations/{org_id}", tags=["Organizations"])
def get_organization_by_id(org_id: str) -> Organization:
    """route get Organization by name"""
    try:
        org_obj_id = ObjectId(org_id)
    except Exception as ex:
        raise HTTPException(
            status_code=401, detail="invalid org_id format"
            ) from ex

    db = get_engine_db()
    org = db.organizations.find_one({"_id": org_obj_id})
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")

    return {
        "organization_id": str(org["_id"]),
        "organization_name": org["organization_name"],
        "email_domain": org["email_domain"],
        "location": org["location"],
        "photo_url": org["photo_url"],
        "users": org["users"],
        "user_count": len(org["users"]),
    }
