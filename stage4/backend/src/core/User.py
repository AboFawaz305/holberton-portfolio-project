"""User model
"""

from pydantic import BaseModel, EmailStr, Field
from pydantic.types import PastDatetime


class User(BaseModel):
    """The representation of a user
    """
    user_id: str
    first_name: str = Field(min_length=3, max_length=25)
    last_name: str = Field(min_length=3, max_length=25)
    username: str = Field(min_length=3, max_length=25)
    email: list[EmailStr]
    created_at: PastDatetime
    updated_at: PastDatetime
