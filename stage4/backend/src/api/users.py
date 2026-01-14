"""Users API endpoints
"""
from datetime import datetime, timezone

from core.NewPatchUser import NewPatchUser
from core.UserAddEmailData import UserAddEmailData
from db import get_engine_db
from fastapi import APIRouter, HTTPException
from services.email_service import (generate_verification_token,
                                    send_verification_email)

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
def add_user_email(user: AuthUser, email:  UserAddEmailData):
    """Add a new email to the user"""
    db = get_engine_db()

    # Check if email already exists
    existing = db.users.find_one({"email.value": email.email})
    if existing:
        raise HTTPException(status_code=422, detail="EMAIL_ALREADY_EXIST")

    # Add email with new structure
    db.users.update_one(
        {"username": user.username},
        {"$push": {"email": {
            "value": email.email,
            "is_verified": False
        }}}
    )

    # Send verification email
    token = generate_verification_token(email.email)
    send_verification_email(email.email, token, user.username)


@users.delete("/emails/{email_id}")
def delete_user_email(user: AuthUser, email_id: int):
    """Delete an email from the user
    """
    if email_id < 0 or email_id >= len(user.email):
        raise HTTPException(status_code=422, detail="EMAIL_DONT_EXIST")

    if len(user.email) == 1:
        raise HTTPException(
            status_code=422, detail="DELETE_ALL_EMAILS_NOT_ALLOWED")

    db = get_engine_db()
    email_to_remove = user.email[email_id].value
    db.users.update_one(
        {"username": user.username},
        {"$pull": {"email": {"value": email_to_remove}}}
    )
