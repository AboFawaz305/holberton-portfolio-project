"""API router definitions of the backend
"""

from datetime import datetime, timedelta, timezone
from os import environ as env
from typing import Annotated

import jwt
from bson.objectid import ObjectId
from dotenv import load_dotenv
from fastapi import Depends, FastAPI
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import ExpiredSignatureError, PyJWTError
from pwdlib import PasswordHash
from pymongo import MongoClient
from pymongo.collection import Collection

from core import NewUser, User

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


@app.get("/")
def read_root():
    """An example hello world route to test that the setup is working"""
    db_client = get_db_connectoin()
    db = db_client.test
    db.collection.insert_one({"msg": "Hello World!"})
    print(db.collection.find({}))
    return {"Hello": "World"}


@app.get("/organizations/{org_id}/groups")
def get_organization_groups(org_id: str):
    """Get all groups for a specific education organization

    Args:
        org_id: The ID of the education organization

    Returns:
        List of groups in the organization
    """
    try:
        db = get_engine_db()
        groups_collection: Collection = db.organizations

        # Find all groups that belong to this organization
        cursor = groups_collection.find({"organization_id": ObjectId(org_id)})

        # Convert MongoDB documents to JSON-serializable format
        groups = []
        for group in cursor:
            # Convert _id to id if it exists, otherwise use the id field
            group_dict = dict(group)
            if "_id" in group_dict:
                group_dict["id"] = str(group_dict["_id"])
                del group_dict["_id"]
            groups.append(group_dict)

        return {"organization_id": org_id, "groups": groups}
    except Exception as e:
        error_msg = f"Error fetching groups: {str(e)}"
        raise HTTPException(status_code=500, detail=error_msg) from e


@app.get("/organizations/{org_id}/groups/{group_id}/resources")
def get_group_resources(org_id: str, group_id: str):
    """Get all resources for a specific group in an organization

    Database Schema:
    Resources are stored in the 'resources' collection with the following structure:
    {
        "id": "resource_id",  # MongoDB _id converted to string
        "group_id": "group_id",  # Reference to the group
        "organization_id": "org_id",  # Reference to the organization
        "name": "Resource Name",
        "description": "Resource description (optional)",
        "type": "file|link|document",  # Type of resource
        "url": "https://...",  # URL or file path
        "created_at": "ISO timestamp",
        "updated_at": "ISO timestamp"
    }

    Args:
        org_id: The ID of the education organization
        group_id: The ID of the group

    Returns:
        List of resources in the group
    """
    try:
        db = get_engine_db()
        resources_collection: Collection = db.resources

        # Find all resources that belong to this group and organization
        query = {"group_id": group_id, "organization_id": org_id}
        cursor = resources_collection.find(query)

        # Convert MongoDB documents to JSON-serializable format
        resources = []
        for resource in cursor:
            # Convert _id to id if it exists
            resource_dict = dict(resource)
            if "_id" in resource_dict:
                resource_dict["id"] = str(resource_dict["_id"])
                del resource_dict["_id"]
            resources.append(resource_dict)

        return {
            "organization_id": org_id,
            "group_id": group_id,
            "resources": resources,
        }
    except Exception as e:
        error_msg = f"Error fetching resources: {str(e)}"
        raise HTTPException(status_code=500, detail=error_msg) from e


@app.post("/register")
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


@app.post("/login")
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


@app.get("/me")
def me_endpoint(user: AuthUser) -> User:
    """route to return user info"""
    return user
