"""Organizations API endpoints
"""
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import List

from bson.objectid import ObjectId
from constants import ORG_PHOTOS_DIR
from core.NewGroupData import NewGroupData
from core.NewOrganizationForm import NewOrganizationForm
from core.Organization import Organization
from db import get_engine_db
from fastapi import Depends
from fastapi.exceptions import HTTPException
from fastapi.routing import APIRouter

from .authentication import AuthUser

orgs = APIRouter(prefix="/organizations", tags=["Organizations"])


@orgs.post("")
async def create_education_organization(
    form: NewOrganizationForm = Depends(NewOrganizationForm.as_form)
):
    """route to create new Organization"""

    db = get_engine_db()
    is_found = db.organizations.find_one(
        {"organization_name": form.organization_name}
    )
    if is_found:
        raise HTTPException(
            status_code=422, detail="Organization already added"
        )

    photo_url = "/api/static/organizations/RR.gif"
    if form.photo and form.photo.filename:

        if form.photo.content_type not in ["image/jpeg", "image/png",
                                           "image/gif"]:
            raise HTTPException(
                status_code=400,
                detail="Only JPEG, PNG, and GIF images are allowed."
            )

        file_extension = Path(form.photo.filename).suffix
        unique_name = f"{int(datetime.now(timezone.utc).timestamp())}"
        unique_name += f"{file_extension}"
        file_path = ORG_PHOTOS_DIR / unique_name

        with file_path.open("wb") as buffer:
            shutil.copyfileobj(form.photo.file, buffer)

        photo_url = f"/api/api/static/organizations/{unique_name}"

    current_time = datetime.now(timezone.utc)
    org_id = db.organizations.insert_one(
        {
            "organization_name": form.organization_name,
            "email_domain": form.email_domain,
            "location": form.location,
            "photo_url": photo_url,
            "members": [],
            "messages": [],
            "_banned_members": [],
            "_created_at": current_time,
            "_updated_at": current_time,
        }
    )
    return {"message": "Organization added successfully",
            "organization_id": str(org_id.inserted_id)}


@orgs.get("")
def get_all_organization() -> List[Organization]:
    """route to get all Organizations"""

    db = get_engine_db()
    orgs_data = db.organizations.find()

    orgs_list = []
    for org in orgs_data:
        user_count = len(org["members"])
        orgs_list.append(
            {
                "organization_id": str(org["_id"]),
                "organization_name": org["organization_name"],
                "email_domain": org["email_domain"],
                "location": org["location"],
                "photo_url": org["photo_url"],
                # "messages": org["messages"],
                "members": org["members"],
                "user_count": user_count,
            }
        )

    return orgs_list


@orgs.get("/{org_id}")
def get_organization_by_id(org_id: str) -> Organization:
    """route get Organization by name"""
    try:
        org_obj_id = ObjectId(org_id)
    except Exception as ex:
        raise HTTPException(
            status_code=401, detail="invalid org_id format"
        ) from ex

    db = get_engine_db()
    org = db.organizations.find_one({"_id": org_obj_id})
    if not org:
        raise HTTPException(status_code=404, detail="ORGANIZATION_NOT_FOUND")

    return Organization(**{
        "organization_id": str(org["_id"]),
        "organization_name": org["organization_name"],
        "email_domain": org["email_domain"],
        "location": org["location"],
        "photo_url": org["photo_url"],
        "messages": org["messages"],
        "members": org["members"],
        "user_count": len(org["members"]),
    })


@orgs.post("/{org_id}/groups")
def create_group(org_id: str, user: AuthUser, new_group: NewGroupData):
    """Create Group in org OR SubGroup in a parent group (single endpoint)

    - If parent_group_id is None => create a main group in the org
    - If parent_group_id exists => create a subgroup inside that parent group
    """

    # 1) validate org_id
    try:
        org_obj_id = ObjectId(org_id)
    except Exception as ex:
        raise HTTPException(
            status_code=401,
            detail="invalid org_id format",
        ) from ex

    db = get_engine_db()

    # 2) ensure org exists
    org = db.organizations.find_one({"_id": org_obj_id})
    if not org:
        raise HTTPException(status_code=404, detail="ORGANIZATION_NOT_FOUND")

    title = new_group.title.strip()
    if len(title) == 0:
        raise HTTPException(status_code=422, detail="INVALID_TITLE")

    current_time = datetime.now(timezone.utc)

    user_obj_id = ObjectId(user.user_id)

    # -------------------------
    # CASE A: Create Group in Org
    # -------------------------
    if not new_group.parent_group_id:
        found = db.groups.find_one(
            {
                "org_id": org_obj_id,
                "title": title,
                "parentGroupId": {"$exists": False},
            }
        )
        if found:
            raise HTTPException(status_code=422, detail="GROUP_ALREADY_EXIST")

        inserted = db.groups.insert_one(
            {
                "title": title,
                "org_id": org_obj_id,
                "messages": [],
                "resources": [],
                "members": [user_obj_id],
                "subGroups": [],
                "AllowedEmailDomains": [],
                "admin": user_obj_id,
                "_created_at": current_time,
                "_updated_at": current_time,
            }
        )
        new_id = inserted.inserted_id

    # -------------------------
    # CASE B: Create SubGroup inside Parent Group
    # -------------------------
    else:
        # validate parent_group_id
        try:
            parent_obj_id = ObjectId(new_group.parent_group_id)
        except Exception as ex:
            raise HTTPException(
                status_code=401,
                detail="invalid parent_group_id format",
            ) from ex

        # parent must exist and belong to same org
        parent = db.groups.find_one(
            {
                "_id": parent_obj_id,
                "org_id": org_obj_id,
            }
        )
        if not parent:
            raise HTTPException(
                status_code=404, detail="PARENT_GROUP_NOT_FOUND")

        # user must be member (entered the group)
        if user_obj_id not in parent.get("members", []):
            raise HTTPException(status_code=403, detail="NOT_A_MEMBER")

        # unique subgroup title under same parent
        found = db.groups.find_one(
            {
                "org_id": org_obj_id,
                "parentGroupId": parent_obj_id,
                "title": title,
            }
        )
        if found:
            raise HTTPException(
                status_code=422, detail="SUBGROUP_ALREADY_EXIST")

        inserted = db.groups.insert_one(
            {
                "title": title,
                "org_id": org_obj_id,
                "parentGroupId": parent_obj_id,
                "messages": [],
                "resources": [],
                "members": [user_obj_id],
                "subGroups": [],
                "AllowedEmailDomains": [],
                "admin": user_obj_id,
                "_created_at": current_time,
                "_updated_at": current_time,
            }
        )

        # link subgroup into parent.subGroups
        db.groups.update_one(
            {"_id": parent_obj_id},
            {
                "$push": {"subGroups": inserted.inserted_id},
                "$set": {"_updated_at": current_time},
            },
        )
        new_id = inserted.inserted_id

    # -------------------------
    # Pipeline: return created group with populated subGroups
    # -------------------------
    pipeline = [
        {"$match": {"_id": new_id}},
        {
            "$lookup": {
                "from": "groups",
                "localField": "subGroups",
                "foreignField": "_id",
                "as": "subGroupsData",
            }
        },
        {
            "$project": {
                "_id": 0,
                "group_id": {"$toString": "$_id"},
                "title": 1,
                "org_id": {"$toString": "$org_id"},
                "parent_group_id": {"$toString": "$parentGroupId"},
                "admin": {"$toString": "$admin"},
                "members": {
                    "$map": {
                        "input": "$members",
                        "as": "m",
                        "in": {"$toString": "$$m"}
                    }
                },
                "subGroups": {
                    "$map": {
                        "input": "$subGroupsData",
                        "as": "sg",
                        "in": {
                            "group_id": {"$toString": "$$sg._id"},
                            "title": "$$sg.title",
                            "admin": "$$sg.admin",
                            "members_count": {"$size": "$$sg.members"},
                        },
                    }
                },
            }
        },
    ]

    result = list(db.groups.aggregate(pipeline))
    return result[0] if result else {}
