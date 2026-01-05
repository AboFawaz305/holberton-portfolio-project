"""Core Functional Utilities
This model contains:
    - Data models defintions
    - functional utility functions
That are commonly used in api routes.
"""
from typing import Annotated
from pydantic import BaseModel, EmailStr, Field
from pydantic.types import PastDatetime
from fastapi import Form, File, UploadFile


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
    user_id: str
    first_name: str = Field(min_length=3, max_length=25)
    last_name: str = Field(min_length=3, max_length=25)
    username: str = Field(min_length=3, max_length=25)
    email: list[EmailStr]
    created_at: PastDatetime
    updated_at: PastDatetime


class LoginUser(BaseModel):
    """The representation of the body of login requests
    """
    username: str = Field(min_length=3, max_length=25)
    password: str = Field(min_length=8, max_length=50)


class NewOrganizationForm(BaseModel):
    """The representation of the
    multi-part form for creating an organization"""
    organization_name: Annotated[str, Form(min_length=3, max_length=25)]
    email_domain: Annotated[str, Form(min_length=3, max_length=25)]
    location: Annotated[str, Form(min_length=3, max_length=25)]
    photo: Annotated[UploadFile | None, File()] = None


class Organization(BaseModel):
    """The representation of an organization"""
    organization_id: str
    organization_name: str = Field(min_length=3, max_length=25)
    email_domain: str = Field(min_length=3, max_length=25)
    location: str = Field(min_length=3, max_length=25)
    photo_url: str | None = None
    users: list
    user_count: int
