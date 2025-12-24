"""API router definitions of the backend
"""
from os import environ as env

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from pymongo.collection import Collection

load_dotenv("../../.env", verbose=True)


def get_db_connection(host=env.get("MONGO_DB_HOST", "database")):
    """Connect to the database
    """
    return MongoClient(host, 27017)


def get_database():
    """Get the main database instance
    """
    db_client = get_db_connection()
    return db_client.education


app = FastAPI()

# Add CORS middleware to allow frontend to access the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    """An example hello world route to test that the setup is working
    """
    db_client = get_db_connection()
    db = db_client.test
    db.collection.insert_one({
        "msg": "Hello World!"
    })
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
        db = get_database()
        groups_collection: Collection = db.groups
        
        # Find all groups that belong to this organization
        cursor = groups_collection.find({"organization_id": org_id})
        
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
        raise HTTPException(status_code=500, detail=f"Error fetching groups: {str(e)}")
