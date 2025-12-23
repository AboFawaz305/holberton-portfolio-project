"""Core Functional Utilities
This model contains:
    - Data models defintions
    - functional utility functions
That are commonly used in api routes.
"""
from pydantic import BaseModel, EmailStr, Field


class NewUser(BaseModel):
    """The representation of the body of registeration requests
    """
    name: str = Field(min_length=2, max_length=50)
    password: str = Field(min_length=8, max_length=50)
    email: EmailStr
