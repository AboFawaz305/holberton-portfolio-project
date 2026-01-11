"""Group API endpoints
"""

from typing import List

from bson.objectid import ObjectId
from core.Group import Groups
from db import get_engine_db
from fastapi.routing import APIRouter


groups = APIRouter(prefix="/groups", tags=["Groups"])


@groups.get("")
def get_all_groups_in_organization(org_id: str) -> List[Groups]:
    """route get all groups in Organization"""
    db = get_engine_db()

    try:
        print(org_id)
        groups_data = db.groups.find({"org_id": ObjectId(org_id)})

        groups_list = []
        for group in groups_data:
            groups_list.append({
                "group_id": str(group["_id"]),
                "title": group["title"],
                "org_id": str(group.get("org_id")),
                "members_count": len(group.get("members", [])),
            })

        return groups_list
    # pylint: disable=broad-exception-caught
    except Exception as e:
        print(f"Error: {e}")
        return []
