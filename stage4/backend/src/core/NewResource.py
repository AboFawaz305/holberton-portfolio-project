"""New Resource schema
"""
from dataclasses import dataclass

from fastapi import UploadFile


@dataclass
class NewResource:
    """New Resource schema
    """
    name: str
    file: UploadFile
    description: str | None = None
