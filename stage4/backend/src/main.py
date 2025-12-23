"""API router definitions of the backend
"""
from os import environ as env

from appwrite.client import Client
from appwrite.exception import AppwriteException
from appwrite.id import ID
from appwrite.services.account import Account
from dotenv import load_dotenv
from fastapi import FastAPI, status
from fastapi.exceptions import HTTPException

from core import NewUser

load_dotenv("../../.env", verbose=True)


def get_client():
    """Get an instance of appwrite client
    """
    client = Client()
    client.set_endpoint(
        f"https://{env.get('APPWRITE_REGION')}.cloud.appwrite.io/v1")
    client.set_project(env.get("APPWRITE_PROJECT_ID"))
    client.set_key(env.get("APPWRITE_API_KEY"))
    return client


app = FastAPI()


@app.post("/register")
def register_endpoint(new_user: NewUser):
    """Create a new account
    """
    ac = Account(get_client())
    try:
        ac.create(
            user_id=ID.unique(),
            **new_user.model_dump()
        )
    except AppwriteException as ae:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT) from ae
