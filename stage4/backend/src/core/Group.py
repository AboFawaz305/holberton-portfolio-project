"""Organizations model
"""
from pydantic import BaseModel, Field


class Group(BaseModel):
    """The representation of an organization"""
    group_id: str
    title: str = Field(min_length=3, max_length=25)
    org_id: str
    members_count: int
