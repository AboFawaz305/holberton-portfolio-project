"""Authentication API endpoints
"""
from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from bson.objectid import ObjectId
from constants import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY
from core.NewUser import NewUser
from core.User import User
from db import get_engine_db
from fastapi import Depends
from fastapi.exceptions import HTTPException
from fastapi.routing import APIRouter
from fastapi.security.oauth2 import (OAuth2PasswordBearer,
                                     OAuth2PasswordRequestForm)
from jwt.exceptions import ExpiredSignatureError, PyJWTError
from pwdlib import PasswordHash

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
auth = APIRouter(prefix="/auth", tags=["Authentication"])
password_hash = PasswordHash.recommended()


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

    # remove the underscore from fields prefixed with an underscore
    found = {("user_id" if k == "_id" else k[1:] if k[0] == "_" else k): v
             for k, v in found.items()}
    found["user_id"] = str(found["user_id"])

    return User(**found)


@auth.post("/register")
def register_endpoint(user: NewUser):
    """Registeration endpoint to create a new user"""
    db = get_engine_db()
    is_found = db.users.find_one(
        {"$or": [{"username": {"$eq": user.username}},
                 {"email": {"$eq": user.email}}
                 ]}
    )
    if is_found:
        raise HTTPException(status_code=422, detail="USER_ALREADY_EXIST")
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


@auth.post("/login")
def login_endpoint(
    user: Annotated[OAuth2PasswordRequestForm, Depends()],
):
    """Login endpoint"""

    db = get_engine_db()

    found = db.users.find_one({"username": user.username})
    if not found:
        raise HTTPException(status_code=401, detail="INVALID_USERNAME")
    if not password_hash.verify(user.password, found["password"]):
        raise HTTPException(status_code=401, detail="INVALID_PASSWORD")

    exp_time = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )
    token = jwt.encode(
        {"user_id": str(found["_id"]), "exp": exp_time},
        SECRET_KEY, algorithm=ALGORITHM
    )
    return {"access_token": token, "token_type": "bearer"}


AuthUser = Annotated[User, Depends(get_current_user)]


@auth.get("/me")
def me_endpoint(user: AuthUser) -> User:
    """route to return user info"""

    return user
