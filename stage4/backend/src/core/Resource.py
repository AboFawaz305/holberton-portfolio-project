"""Resource model
"""
from pydantic import BaseModel, Field
from pydantic.types import PastDatetime


class Resource(BaseModel):
    """The representation of a resource in a group"""
    resource_id: str
    name: str = Field(min_length=3, max_length=50)
    description: str | None = Field(max_length=150, default=None)
    file_url:  str
    uploaded_by: str
    rating: int = Field(ge=-1, le=5, default=-1)  # -1 means unrated
    created_at: PastDatetime
