"""Group API endpoints
"""

import shutil
import uuid
from datetime import datetime, timezone
from typing import List

from bson.objectid import ObjectId
from constants import GROUPS_RESOURCES_DIR
from core.Group import Group
from db import get_engine_db
from fastapi import Form, Path, UploadFile
from fastapi.exceptions import HTTPException
from fastapi.routing import APIRouter

from api.authentication import AuthUser

groups = APIRouter(prefix="/groups", tags=["Groups"])


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

    groups_data = list(db.groups.find({"org_id": org_obj_id}))

    groups_list = []
    for group in groups_data:
        groups_list.append({
            "group_id": str(group["_id"]),
            "title": group["title"],
            "org_id": str(group. get("org_id")),
            "members_count":  len(group.get("members", [])),
        })

    return groups_list


@groups.get("/{group_id}")
def get_group_by_id(group_id: str):
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

    return {
        "group_id": str(group["_id"]),
        "title": group["title"],
        "org_id": str(group["org_id"]),
        "members_count": len(group. get("members", [])),
    }


@groups.get("/{group_id}/subgroups")
def get_subgroups_of_group(group_id: str):
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

    subgroup_ids = parent_group.get("subGroups", [])

    if not subgroup_ids:
        return []

    # Convert string IDs to ObjectIds
    subgroup_obj_ids = []
    for sub_id in subgroup_ids:
        try:
            if isinstance(sub_id, str):
                subgroup_obj_ids.append(ObjectId(sub_id))
            else:
                subgroup_obj_ids.append(sub_id)
        # pylint: disable=broad-exception-caught
        except Exception:
            continue

    subgroups_data = db.groups.find({"_id": {"$in": subgroup_obj_ids}})

    subgroups_list = []
    for group in subgroups_data:
        subgroups_list.append({
            "group_id":  str(group["_id"]),
            "title": group["title"],
            "org_id":  str(group["org_id"]),
            "members_count":  len(group.get("members", [])),
        })

    return subgroups_list


@groups.post("{gid}/resources")
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
    file_url = f"/api/static/groups/resources/{unique_filename}"
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
