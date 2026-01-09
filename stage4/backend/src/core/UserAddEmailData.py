"""UserAddEmailData model
"""

from pydantic import BaseModel, EmailStr


class UserAddEmailData(BaseModel):
    """The representation of data to add an email
    """
    email: EmailStr
