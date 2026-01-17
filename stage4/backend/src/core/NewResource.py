"""New Resource schema
"""

from fastapi import UploadFile
from pydantic import BaseModel


class NewResource(BaseModel):
    """New Resource schema
    """
    name: str
    file: UploadFile
    description: str | None = None
