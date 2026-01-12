"""Users API endpoints
"""
from datetime import datetime, timezone

from bson.objectid import ObjectId
from core.NewPatchUser import NewPatchUser
from core.UserAddEmailData import UserAddEmailData
from db import get_engine_db
from fastapi import APIRouter, HTTPException

from .authentication import AuthUser, password_hash

users = APIRouter(prefix="/users", tags=["Users"])


@users.patch("")
def patch_update_user(user: AuthUser, new_user: NewPatchUser):
    """Update the fields in user based on the given fields in new_user
    """
    values_to_update = new_user.model_dump(
        exclude_unset=True, exclude_none=True)
    if len(values_to_update.keys()) == 0:
        return
    db = get_engine_db()
    if "username" in values_to_update.keys():
        found = db.users.find_one({"username": values_to_update['username']})
        if found is not None:
            raise HTTPException(
                status_code=422, detail="USERNAME_ALREADY_EXIST")
    if "password" in values_to_update.keys():
        values_to_update["password"] = password_hash.hash(
            values_to_update["password"])
    db.users.update_one({"username": {"$eq": user.username}}, {
        "$set": {
            **values_to_update,
            **{"_updated_at": datetime.now(timezone.utc)}
        }
    })


@users.post("/emails")
def add_user_email(user: AuthUser, email: UserAddEmailData):
    """Add a new email to the user
    """
    db = get_engine_db()
    pipeline = [
        {"$unwind": "$email"},
        {
            "$group": {
                "_id": None,
                "emails": {"$addToSet": "$email"}
            }
        },
        {"$project": {"_id": 0, "emails": 1}}
    ]

    result = list(db.users.aggregate(pipeline))
    print(result)
    if email.email in result[0]["emails"]:
        raise HTTPException(status_code=422, detail="EMAIL_ALREADY_EXIST")
    db.users.update_one(
        {"username": user.username},
        {"$push": {"email": email.email}}
    )


@users.delete("/emails/{email_id}")
def delete_user_email(user: AuthUser, email_id: int):
    """Delete an email from the user
    """
    if email_id >= len(user.email):
        raise HTTPException(status_code=422, detail="EMAIL_DONT_EXIST")
    if len(user.email) == 1:
        raise HTTPException(
            status_code=422, detail="DELETE_ALL_EMAILS_NOT_ALLOWED")
    db = get_engine_db()
    db.users.update_one(
        {"username": user.username},
        {"$pull": {"email": user.email[email_id]}}
    )


@users.post("/groups/{gid}")
def join_group(user: AuthUser, gid: str, is_org: bool):
    """Join a user to a group
    """
    db = get_engine_db()
    found = True
    if is_org:
        found = db.organizations.find_one({"_id": ObjectId(gid)})
    else:
        found = db.groups.find_one({"_id": ObjectId(gid)})
    if not found:
        raise HTTPException(
            status_code=422, detail="ORGANIZATION_NOT_FOUND")
    if user.username in found["members"]:
        raise HTTPException(status_code=422, detail="USER_ALREADY_JOINED")
    if is_org:
        db.organizations.update_one(
            {"_id": ObjectId(gid)}, {"$addToSet": {"members": user.username}})
    else:
        db.groups.update_one(
            {"_id": ObjectId(gid)}, {"$addToSet": {"members": user.username}})


@users.get("/groups/{gid}/join_status")
def is_joined_to_group(user: AuthUser, gid: str, is_org: bool):
    """Join a user to a group
    """
    db = get_engine_db()
    found = True
    if is_org:
        found = db.organizations.find_one({"_id": ObjectId(gid)})
    else:
        found = db.groups.find_one({"_id": ObjectId(gid)})
    if not found:
        raise HTTPException(
            status_code=422, detail="ORGANIZATION_NOT_FOUND")
    if user.username in found["members"]:
        return {"msg": "yes"}
    return {"msg": "no"}
