"""Core Functional Utilities
This model contains:
    - Data models defintions
    - functional utility functions
That are commonly used in api routes.
"""
from typing import Any

from fastapi import UploadFile, WebSocket
from pydantic import BaseModel, EmailStr, Field, model_validator
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


class Organization(BaseModel):
    """The representation of an organization"""
    organization_id: str
    organization_name: str = Field(min_length=3, max_length=25)
    email_domain: str = Field(min_length=3, max_length=25)
    location: str = Field(min_length=3, max_length=25)
    photo_url: str | None = None
    # messages: list
    users: list
    user_count: int


class ConnectionManager:
    """ manager class for websocket connections"""

    def __init__(self):
        self.active_connections: dict[str, list[WebSocket]] = {}

    def connect(self, websocket: WebSocket, org_id: str):
        """add a websocket to an org"""
        if org_id not in self.active_connections:
            self.active_connections[org_id] = []
        self.active_connections[org_id].append(websocket)

    def disconnect(self, websocket: WebSocket, org_id: str):
        """removes a websocket connection"""
        if org_id in self.active_connections:
            if websocket in self.active_connections[org_id]:
                self.active_connections[org_id].remove(websocket)
            if not self.active_connections[org_id]:
                del self.active_connections[org_id]

    async def send_personal_message(self, message, websocket: WebSocket):
        """send to self a massage"""
        await websocket.send_json(message)

    async def broadcast(self, message_payload: dict, org_id: str):
        """broadcast a massage to all websockets with same org_id"""
        if org_id in self.active_connections:
            for connection in self.active_connections[org_id]:
                await connection.send_json(message_payload)


class NewPatchUser(BaseModel, extra="forbid"):
    """The representation of a user
    Extra fields are not permitted
    """
    first_name: str | None = Field(min_length=3, max_length=25, default=None)
    last_name: str | None = Field(min_length=3, max_length=25, default=None)
    username: str | None = Field(min_length=3, max_length=25, default=None)
    password: str | None = Field(min_length=8, max_length=50, default=None)
