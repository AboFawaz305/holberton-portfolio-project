"""Core Functional Utilities
This model contains:
    - Data models defintions
    - functional utility functions
That are commonly used in api routes.
"""
from typing import Annotated, Literal
from pydantic import BaseModel, EmailStr, Field
from pydantic.types import PastDatetime
from fastapi import File, UploadFile, WebSocket, WebSocketDisconnect, WebSocketException


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
    def __init__(self):
        self.active_connections: dict[str,list[WebSocket]] = {}

    def connect(self, websocket: WebSocket, org_id:str):
        if org_id not in self.active_connections:
            self.active_connections[org_id] = []
        self.active_connections[org_id].append(websocket)

    def disconnect(self, websocket: WebSocket, org_id:str):
        if org_id in self.active_connections:
            if websocket in self.active_connections[org_id]:
                self.active_connections[org_id].remove(websocket)
            if not self.active_connections[org_id]:
                del self.active_connections[org_id]

    
    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message_payload: dict, org_id:str):
        if org_id in self.active_connections:
            for connection in self.active_connections[org_id]:
                await connection.send_json(message_payload)