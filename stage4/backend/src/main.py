"""API router definitions of the backend
"""
from os import environ as env

from dotenv import load_dotenv
from fastapi import FastAPI
from pymongo import MongoClient

load_dotenv("../../.env", verbose=True)


def get_db_connectoin(host=env.get("MONGO_DB_HOST", "database")):
    """Connect to the database
    """

    return MongoClient(host, 27017)


app = FastAPI()


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
