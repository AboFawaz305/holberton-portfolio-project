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
    email: list[EmailStr]
    _created_at: PastDatetime
    _updated_at: PastDatetime


class LoginUser(BaseModel):
    """The representation of the body of login requests
    """
    username: str = Field(min_length=3, max_length=25)
    password: str = Field(min_length=8, max_length=50)


class NewOrg(BaseModel):
    """The representation of the body
    Createing a education organization requests
    """
    organization_name: str = Field(min_length=3, max_length=25)
    email_domain: str = Field(min_length=3, max_length=25)
    location: str = Field(min_length=3, max_length=25)


class Org(BaseModel):
    """The representation of an ORG"""
    organization_name: str = Field(min_length=3, max_length=25)
    email_domain: str = Field(min_length=3, max_length=25)
    location: str = Field(min_length=3, max_length=25)
    users: list
    user_count: int
