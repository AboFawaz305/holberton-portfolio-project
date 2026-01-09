"""Organizations model
"""
from pydantic import BaseModel, Field


class Organization(BaseModel):
    """The representation of an organization"""
    organization_id: str
    organization_name: str = Field(min_length=3, max_length=25)
    email_domain: str = Field(min_length=3, max_length=25)
    location: str = Field(min_length=3, max_length=25)
    photo_url: str | None = None
    # messages: list
    users: list
    user_count: int
