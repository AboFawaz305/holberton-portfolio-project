"""NewOrganizationForm model
"""

from fastapi import Form, UploadFile
from pydantic import BaseModel, Field


class NewOrganizationForm(BaseModel):
    """model for new org"""
    organization_name: str = Field(min_length=3, max_length=25)
    email_domain: str = Field(min_length=3, max_length=25)
    location: str = Field(min_length=3, max_length=25)
    photo: UploadFile | None = None

    @classmethod
    def as_form(
        cls,
        organization_name: str = Form(..., min_length=3, max_length=25),
        email_domain: str = Form(..., min_length=3, max_length=25),
        location: str = Form(..., min_length=3, max_length=25),
        photo: UploadFile | None = None
    ):
        """model for new org"""
        return cls(
            organization_name=organization_name,
            email_domain=email_domain,
            location=location,
            photo=photo
        )
