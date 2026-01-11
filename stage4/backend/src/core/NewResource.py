from dataclasses import dataclass

from fastapi import UploadFile


@dataclass
class NewResource:
    name: str
    file: UploadFile
    description: str | None = None
