"""API router definitions of the backend
"""
from datetime import datetime, timezone
from os import environ as env

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.exceptions import HTTPException
from pwdlib import PasswordHash
from pymongo import MongoClient

from core import NewUser

load_dotenv("../../.env", verbose=True)


def get_db_connectoin(host=env.get("MONGO_DB_HOST", "database")):
    """Connect to the database
    """

    return MongoClient(host, 27017)


def get_engine_db():
    """Get an instance from the main database for the backend
    """
    return get_db_connectoin().engine


app = FastAPI()
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
