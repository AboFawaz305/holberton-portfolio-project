"""API router definitions of the backend
"""

from datetime import datetime, timedelta, timezone
from os import environ as env
from typing import Annotated, List

import jwt
from bson.objectid import ObjectId
from dotenv import load_dotenv
from fastapi import Depends, FastAPI
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import ExpiredSignatureError, PyJWTError
from pwdlib import PasswordHash
from pymongo import MongoClient

from core import NewUser, User, NewOrganization, Organization

load_dotenv("../../.env", verbose=True)

SECRET_KEY = "wow_secret_KEY"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

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


@app.post("/register", tags=["User"])
def register_endpoint(user: NewUser):
    """Registeration endpoint to create a new user"""
    db = get_engine_db()
    is_found = db.users.find_one(
        {"$or": [{"username": {"$eq": user.username}},
                 {"email": {"$eq": user.email}}]}
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
        SECRET_KEY,
        algorithm=ALGORITHM
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
            "updated_at": user["_updated_at"]
        }


@app.post("/organizations", tags=["Organizations"])
def create_education_organization(org: NewOrganization):
    """route to create new Organization"""
    db = get_engine_db()
    is_found = db.orgs.find_one({"organization_name": org.organization_name})
    if is_found:
        raise HTTPException(
            status_code=422, detail="Organization already added"
            )
    current_time = datetime.now(timezone.utc)
    db.orgs.insert_one(
        {
            "organization_name": org.organization_name,
            "email_domain": org.email_domain,
            "location": org.location,
            "users": [],
            "_banned_users": [],
            "_created_at": current_time,
            "_updated_at": current_time,
        }
        )
    return {"message": "Organization added successfully"}


@app.get("/organizations", tags=["Organizations"])
def get_all_organization() -> List[Organization]:
    """ route to get all Organizations
    """

    db = get_engine_db()
    orgs_data = db.orgs.find()

    orgs_list = []
    for org in orgs_data:
        user_count = len(org["users"])
        orgs_list.append({
            "organization_name": org["organization_name"],
            "email_domain": org["email_domain"],
            "location": org["location"],
            "users": org["users"],
            "user_count": user_count
        })

    return orgs_list


@app.get("/organizations/{org_name}", tags=["Organizations"])
def get_organization_by_name(org_name: str) -> Organization:
    """route get Organization by name
    """

    db = get_engine_db()
    org = db.orgs.find_one({"organization_name": org_name})
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")

    return {
            "organization_name": org["organization_name"],
            "email_domain": org["email_domain"],
            "location": org["location"],
            "users": org["users"],
            "user_count": len(org["users"])
        }
