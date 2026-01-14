"""Group API endpoints
"""

import shutil
import uuid
from datetime import datetime, timezone
from pathlib import Path

from bson.objectid import ObjectId
from constants import GROUPS_RESOURCES_DIR
from db import get_engine_db
from fastapi import Form, UploadFile
from fastapi.exceptions import HTTPException
from fastapi.routing import APIRouter

from .authentication import AuthUser

groups = APIRouter(prefix="/groups", tags=["Groups"])


def check_group_access(user: AuthUser, allowed_domains: list[str]):
    """Check if user can access group based on email domain
    Returns None if access granted, raises HTTPException otherwise
    """
    # No restrictions - allow everyone
    if not allowed_domains:
        return

    # Check all user emails
    has_matching_domain = False
    has_verified_matching = False

    for email in user.email:
        domain = email.value.split("@")[1].lower()
        if domain in [d.lower() for d in allowed_domains]:
            has_matching_domain = True
            if email.is_verified:
                has_verified_matching = True
                break

    # User has verified email with allowed domain - grant access
    if has_verified_matching:
        return

    # User has matching domain but not verified
    if has_matching_domain:
        raise HTTPException(status_code=403, detail="EMAIL_NOT_VERIFIED")

    # User has no email with allowed domain
    raise HTTPException(status_code=403, detail="EMAIL_DOMAIN_NOT_ALLOWED")


@groups.get("/org/{org_id}")
def get_all_groups_in_organization(org_id: str):
    """Get all groups in an Organization"""
    db = get_engine_db()

    try:
        org_obj_id = ObjectId(org_id)
    except Exception as ex:
        raise HTTPException(
            status_code=400, detail="Invalid org_id format"
        ) from ex

    query = {
        "org_id": org_obj_id,
        "$or": [
            {"parentGroupId": {"$exists": False}},
            {"parentGroupId": None},
            {"parentGroupId": ""}
        ]
    }

    groups_data = list(db.groups.find(query))

    groups_list = []
    for group in groups_data:
        groups_list.append({
            "group_id": str(group["_id"]),
            "title": group["title"],
            "org_id": str(group.get("org_id", "")),
            "members_count": len(group.get("members", [])),
        })

    return groups_list


@groups.get("/{group_id}")
def get_group_by_id(group_id: str, user: AuthUser):
    """Get a group by its ID"""
    db = get_engine_db()

    try:
        group_obj_id = ObjectId(group_id)
    except Exception as ex:
        raise HTTPException(
            status_code=400, detail="Invalid group_id format"
        ) from ex

    group = db.groups.find_one({"_id": group_obj_id})
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")

    check_group_access(user, group.get("AllowedEmailDomains", []))

    return {
        "group_id": str(group["_id"]),
        "title": group["title"],
        "org_id": str(group.get("org_id", "")),
        "parentGroupId": (
            str(group["parentGroupId"])
            if group.get("parentGroupId")
            else None
        ),
        "members_count": len(group.get("members", [])),
    }


@groups.get("/{group_id}/subgroups")
def get_subgroups_of_group(group_id: str, user: AuthUser):
    """Get all subgroups of a group"""
    db = get_engine_db()

    try:
        group_obj_id = ObjectId(group_id)
    except Exception as ex:
        raise HTTPException(
            status_code=400, detail="Invalid group_id format"
        ) from ex

    parent_group = db.groups.find_one({"_id": group_obj_id})
    if not parent_group:
        raise HTTPException(status_code=404, detail="Group not found")

    check_group_access(user, parent_group.get("AllowedEmailDomains", []))

    subgroup_ids = parent_group.get("subGroups", [])

    if not subgroup_ids:
        return []

    subgroup_obj_ids = []
    for sub_id in subgroup_ids:
        try:
            subgroup_obj_ids.append(ObjectId(sub_id)
                                    if isinstance(sub_id, str)
                                    else sub_id
                                    )
        # pylint: disable=broad-exception-caught
        except Exception:
            continue

    subgroups_data = db.groups.find({"_id": {"$in": subgroup_obj_ids}})

    subgroups_list = []
    for group in subgroups_data:
        subgroups_list.append({
            "group_id": str(group["_id"]),
            "title": group["title"],
            "org_id": str(group.get("org_id", "")),
            "members_count": len(group.get("members", [])),
        })

    return subgroups_list


@groups.post("/{gid}/resources")
def add_new_resource_to_a_groupa(
    user: AuthUser,
    gid: str,
    name: str = Form(..., min_length=3, max_length=50),
    file: UploadFile = Form(...),
    description: str | None = Form(None, max_length=150),
):
    """Add a new resource to a group"""

    # Validate group ObjectId format
    try:
        group_obj_id = ObjectId(gid)
    except Exception as ex:
        raise HTTPException(
            status_code=400, detail="INVALID_GROUP_ID_FORMAT"
        ) from ex

    db = get_engine_db()

    # Check if group exists
    group = db.groups.find_one({"_id": group_obj_id})
    if not group:
        raise HTTPException(status_code=404, detail="GROUP_NOT_FOUND")

    # Check if user is a member
    if user.username not in group.get("members", []):
        raise HTTPException(status_code=403, detail="USER_NOT_A_MEMBER")

    # Generate unique filename:  timestamp_uuid. extension
    file_extension = Path(file.filename).suffix if file. filename else ""
    timestamp = int(datetime.now(timezone. utc).timestamp())
    unique_id = uuid.uuid4().hex
    unique_filename = f"{timestamp}_{unique_id}{file_extension}"

    # Ensure directory exists
    GROUPS_RESOURCES_DIR.mkdir(parents=True, exist_ok=True)

    # Save file to disk
    file_path = GROUPS_RESOURCES_DIR / unique_filename
    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Create resource document
    file_url = f"/api/{GROUPS_RESOURCES_DIR}/{unique_filename}"
    current_time = datetime.now(timezone.utc)
    new_resource = {
        "_id":  ObjectId(),
        "name":  name,
        "description": description,
        "file_url": file_url,
        "uploaded_by": user.username,
        "rating": -1,
        "_created_at": current_time,
    }

    # Push resource to group's resources array
    db.groups.update_one(
        {"_id": group_obj_id},
        {"$push":  {"resources": new_resource}}
    )


@groups.get("/{gid}/resources")
def get_resources(gid: str):
    """Get all resources belonging to a group
    """
    db = get_engine_db()

    try:
        group_obj_id = ObjectId(gid)
    except Exception as ex:
        raise HTTPException(
            status_code=400, detail="Invalid group_id format") from ex

    group = db.groups.find_one({"_id": group_obj_id})
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    resources = group.get("resources")
    for r in resources:
        r["_id"] = str(r["_id"])
    return resources
