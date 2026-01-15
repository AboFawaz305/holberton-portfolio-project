"""NewGroupData model
"""
from typing import Optional

from pydantic import BaseModel, Field


class NewGroupData(BaseModel, extra="forbid"):
    """The representation of a group
    Extra fields are not permitted
    """
    title: str = Field(min_length=3, max_length=100)
    parent_group_id: Optional[str] = None
