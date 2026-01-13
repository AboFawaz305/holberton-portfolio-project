"""Group API endpoints
"""


from bson. objectid import ObjectId
from db import get_engine_db
from fastapi import HTTPException
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
        "org_id": str(group["org_id"]),
        "members_count": len(group.get("members", [])),
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
