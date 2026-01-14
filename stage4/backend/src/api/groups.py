"""Group API endpoints
"""


from bson. objectid import ObjectId
from db import get_engine_db
from fastapi import HTTPException
from fastapi. routing import APIRouter


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
