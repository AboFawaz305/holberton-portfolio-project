"""User model
"""

from pydantic import BaseModel, EmailStr, Field
from pydantic.types import PastDatetime


class UserEmail(BaseModel):
    """Email with verification status"""
    value: EmailStr
    is_verified: bool = False

class User(BaseModel):
    """The representation of a user
    """
    user_id: str
    first_name: str = Field(min_length=3, max_length=25)
    last_name: str = Field(min_length=3, max_length=25)
    username: str = Field(min_length=3, max_length=25)
    email: list[UserEmail]
    created_at: PastDatetime
    updated_at: PastDatetime
