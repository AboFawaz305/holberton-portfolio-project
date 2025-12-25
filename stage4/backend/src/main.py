"""API router definitions of the backend
"""
from datetime import datetime, timezone
from os import environ as env
from typing import Annotated

import jwt
from dotenv import load_dotenv
from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.exceptions import HTTPException
from pwdlib import PasswordHash
from pymongo import MongoClient

from core import NewUser, LoginUser, User


load_dotenv("../../.env", verbose=True)

SECRET_KEY = "wow_secret_KEY"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(token : Annotated[str, Depends(oauth2_scheme)]):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    user_id = payload.get("user_id")
    if not user_id:
        raise HTTPException(status_code=401, detail="token missing user_id")
    return db.users.find_one({"_id":user_id})

authuser = Annotated[User, Depends(get_current_user)]

def get_db_connectoin(host=env.get("MONGO_DB_HOST", "database")):
    """Connect to the database
    """

    return MongoClient(host, 27017)


def get_engine_db():
    """Get an instance from the main database for the backend
    """
    return get_db_connectoin().engine


app = FastAPI(root_path="/api")
password_hash = PasswordHash.recommended()


@app.get("/")
def read_root():
    """An example hello world route to test that the setup is working
    """
    db_client = get_db_connectoin()
    db = db_client.test
    db.collection.insert_one({
        "msg": "Hello World!"
    })
    print(db.collection.find({}))
    return {"Hello": "World"}


@app.post("/register")
def register_endpoint(user: NewUser):
    """Registeration endpoint to create a new user
    """
    db = get_engine_db()
    is_found = db.users.find_one(
        {"$or": [
            {"username": {"$eq": user.username}},
            {"email": {"$eq": user.email}}
        ]})
    if is_found:
        raise HTTPException(status_code=422, detail="User Already Exists.")
    current_time = datetime.now(timezone.utc)
    db.users.insert_one({
        "username": user.username,
        "email": user.email,
        "password": password_hash.hash(user.password),
        "first_name": user.first_name,
        "last_name": user.last_name,
        "_created_at": current_time,
        "_updated_at": current_time
    })

@app.post("/login")
def login_endpoint(user : Annotated[OAuth2PasswordRequestForm, Depends()],):
    """Login endpoint
    """

    db = get_engine_db()

    found =  db.users.find_one({"username":user.username})
    if not found:
        raise HTTPException(status_code=401, detail="invalid username")
    if not password_hash.verify(user.password, found["password"]):
        raise HTTPException(status_code=401, detail="invalid password")
    
    return {"token": jwt.encode({"user_id":str(found["_id"])},SECRET_KEY,algorithm=ALGORITHM)}

@app.get("/me")
def me_endpoint(user: authuser)-> User:
    return user
    