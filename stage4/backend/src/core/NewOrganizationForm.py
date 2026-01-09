"""NewOrganizationForm model
"""
from typing import Any

from fastapi import UploadFile
from pydantic import BaseModel, Field
from pydantic.functional_validators import model_validator


class NewOrganizationForm(BaseModel):
    """The representation of the
    multi-part form for creating an organization"""
    organization_name: str = Field(min_length=3, max_length=25)
    email_domain: str = Field(min_length=3, max_length=25)
    location: str = Field(min_length=3, max_length=25)
    photo: UploadFile | None = None

    @model_validator(mode='before')
    @classmethod
    def check_card_number_not_present(cls, data: Any) -> Any:
        """ to check the req photo set to none if not there"""
        if isinstance(data, dict):
            if 'photo' in data and data["photo"] == "":
                data["photo"] = None
        return data
