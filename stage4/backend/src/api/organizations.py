"""Organizations API endpoints
"""
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Annotated, List

from bson.objectid import ObjectId
from constants import ORG_PHOTOS_DIR
from core.NewOrganizationForm import NewOrganizationForm
from core.Organization import Organization
from db import get_engine_db
from fastapi import Form
from fastapi.exceptions import HTTPException
from fastapi.routing import APIRouter

orgs = APIRouter(prefix="/organizations", tags=["Organizations"])


@orgs.post("")
async def create_education_organization(
    form: Annotated[NewOrganizationForm, Form()]
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

        photo_url = f"/api/static/organizations/{unique_name}"

    current_time = datetime.now(timezone.utc)
    org_id = db.organizations.insert_one(
        {
            "organization_name": form.organization_name,
            "email_domain": form.email_domain,
            "location": form.location,
            "photo_url": photo_url,
            "users": [],
            "messages": [],
            "groups": [],
            "_banned_users": [],
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
        user_count = len(org["users"])
        orgs_list.append(
            {
                "organization_id": str(org["_id"]),
                "organization_name": org["organization_name"],
                "email_domain": org["email_domain"],
                "location": org["location"],
                "photo_url": org["photo_url"],
                # "messages": org["messages"],
                "users": org["users"],
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
        "users": org["users"],
        "user_count": len(org["users"]),
    })
