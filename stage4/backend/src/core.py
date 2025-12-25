"""Core Functional Utilities
This model contains:
    - Data models defintions
    - functional utility functions
That are commonly used in api routes.
"""
from pydantic import BaseModel, EmailStr, Field
from pydantic.types import PastDatetime


class NewUser(BaseModel):
    """The representation of the body of registeration requests
    """
    first_name: str = Field(min_length=3, max_length=25)
    last_name: str = Field(min_length=3, max_length=25)
    username: str = Field(min_length=3, max_length=25)
    email: EmailStr
    password: str = Field(min_length=8, max_length=50)


class User(BaseModel):
    """The representation of a user
    """
    first_name: str = Field(min_length=3, max_length=25)
    last_name: str = Field(min_length=3, max_length=25)
    username: str = Field(min_length=3, max_length=25)
    email: EmailStr
    _created_at: PastDatetime
    _updated_at: PastDatetime
