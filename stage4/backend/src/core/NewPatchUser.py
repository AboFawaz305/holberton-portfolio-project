"""NewPatchUser model
"""
from pydantic import BaseModel, Field


class NewPatchUser(BaseModel, extra="forbid"):
    """The representation of a user
    Extra fields are not permitted
    """
    first_name: str | None = Field(min_length=3, max_length=25, default=None)
    last_name: str | None = Field(min_length=3, max_length=25, default=None)
    username: str | None = Field(min_length=3, max_length=25, default=None)
    password: str | None = Field(min_length=8, max_length=50, default=None)
