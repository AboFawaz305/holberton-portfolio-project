"""API router definitions of the backend
"""
from os import environ as env

from appwrite.client import Client
from dotenv import load_dotenv
from fastapi import FastAPI

load_dotenv("../../.env", verbose=True)

client = Client()
client.set_endpoint(
    f"https://{env.get('APPWRITE_REGION')}.cloud.appwrite.io/v1")
client.set_project(env.get("APPWRITE_PROJECT_ID"))
client.set_key(env.get("APPWRITE_API_KEY"))


app = FastAPI()


@app.get("/")
def read_root():
    """An example hello world route to test that the setup is working
    """
    return {"Hello": "World"}
