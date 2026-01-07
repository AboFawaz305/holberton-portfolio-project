"""API router definitions of the backend
"""

import shutil
from datetime import datetime, timedelta, timezone
from os import environ as env
from pathlib import Path
from typing import Annotated, List

import jwt
from bson.objectid import ObjectId
from dotenv import load_dotenv
from fastapi import (Depends, FastAPI, Form, WebSocket, WebSocketDisconnect,
                     status)
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.staticfiles import StaticFiles
from jwt.exceptions import ExpiredSignatureError, PyJWTError
from pwdlib import PasswordHash
from pymongo import MongoClient

from core import (ConnectionManager, NewOrganizationForm, NewPatchUser,
                  NewUser, Organization, User)

load_dotenv("../../.env", verbose=True)

SECRET_KEY = "wow_secret_KEY"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

BASE_DIR = Path(__file__).resolve().parent
UPLOAD_DIR = BASE_DIR / "uploads"
ORG_PHOTOS_DIR = UPLOAD_DIR / "organizations"
ORG_PHOTOS_DIR.mkdir(parents=True, exist_ok=True)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    """token check"""

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except ExpiredSignatureError as es:
        raise HTTPException(status_code=401, detail="token expired") from es
    except PyJWTError as je:
        raise HTTPException(status_code=401, detail="invalid token") from je

    user_id = payload.get("user_id")
    if not user_id:
        raise HTTPException(status_code=401, detail="token missing user_id")

    try:
        object_id = ObjectId(user_id)
    except Exception as ex:
        raise HTTPException(
            status_code=401, detail="invalid user_id format"
        ) from ex

    db = get_engine_db()
    found = db.users.find_one({"_id": object_id})
    if not found:
        raise HTTPException(status_code=401, detail="user not in Database")

    # remove the underscore from fields prefixed with an underscore
    found = {("user_id" if k == "_id" else k[1:] if k[0] == "_" else k): v
             for k, v in found.items()}
    found["user_id"] = str(found["user_id"])

    return User(**found)


AuthUser = Annotated[User, Depends(get_current_user)]


def get_db_connection(host=env.get("MONGO_DB_HOST", "localhost")):
    """Connect to the database"""

    return MongoClient(host, 27017)


def get_engine_db():
    """Get an instance from the main database for the backend"""
    return get_db_connection().engine


def get_organization_messages_with_users(org_id):
    """gets orgs messages with users"""

    db = get_engine_db()

    pipeline = [
        {"$match": {"_id": ObjectId(org_id)}},
        {"$unwind": "$messages"},
        {
            "$lookup": {
                "from": "users",
                "localField": "messages.sender_id",
                "foreignField": "_id",
                "as": "sender_info"
            }
        },
        {"$unwind": "$sender_info"},
        {
            "$project": {
                "_id": 0,
                "message_id": {"$toString": "$messages._id"},
                "content": "$messages.content",
                "timestamp": {
                    "$dateToString": {
                        "format": "%Y-%m-%d %H:%M:%S",
                        "date": "$messages.timestamp"
                    }
                },
                "user": {
                    "_id": {"$toString": "$sender_info._id"},
                    "username": "$sender_info.username",
                    # "photo_url": "$sender_info.photo_url"
                }
            }
        }
    ]

    return list(db.organizations.aggregate(pipeline))


app = FastAPI(root_path="/api")
password_hash = PasswordHash.recommended()
app.mount("/static", StaticFiles(directory=UPLOAD_DIR), name="static")

manager = ConnectionManager()


@app.get("/")
def read_root():
    """An example hello world route to test that the setup is working"""
    db_client = get_db_connection()
    db = db_client.test
    db.collection.insert_one({"msg": "Hello World!"})
    return {"Hello": "World"}


@app.post("/register")
def register_endpoint(user: NewUser):
    """Registeration endpoint to create a new user"""
    db = get_engine_db()
    is_found = db.users.find_one(
        {"$or": [{"username": {"$eq": user.username}},
                 {"email": {"$eq": user.email}}
                 ]}
    )
    if is_found:
        raise HTTPException(status_code=422, detail="USER_ALREADY_EXIST")
    current_time = datetime.now(timezone.utc)
    db.users.insert_one(
        {
            "username": user.username,
            "email": [user.email],
            "password": password_hash.hash(user.password),
            "first_name": user.first_name,
            "last_name": user.last_name,
            "_created_at": current_time,
            "_updated_at": current_time,
        }
    )


@app.post("/login", tags=["User"])
def login_endpoint(
    user: Annotated[OAuth2PasswordRequestForm, Depends()],
):
    """Login endpoint"""

    db = get_engine_db()

    found = db.users.find_one({"username": user.username})
    if not found:
        raise HTTPException(status_code=401, detail="INVALID_USERNAME")
    if not password_hash.verify(user.password, found["password"]):
        raise HTTPException(status_code=401, detail="INVALID_PASSWORD")

    exp_time = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )
    token = jwt.encode(
        {"user_id": str(found["_id"]), "exp": exp_time},
        SECRET_KEY, algorithm=ALGORITHM
    )
    return {"access_token": token, "token_type": "bearer"}


@app.get("/me", tags=["User"])
def me_endpoint(user: AuthUser) -> User:
    """route to return user info"""

    return user


@app.post("/organizations", tags=["Organizations"])
async def create_education_organization(
    form: Annotated[NewOrganizationForm, Form()]
):
    """route to create new Organization"""

    db = get_engine_db()
    is_found = db.organizations.find_one(
        {"organization_name": form.organization_name}
    )
    if is_found:
        raise HTTPException(
            status_code=422, detail="Organization already added"
        )

    photo_url = "/api/static/organizations/RR.gif"
    if form.photo and form.photo.filename:

        if form.photo.content_type not in ["image/jpeg", "image/png",
                                           "image/gif"]:
            raise HTTPException(
                status_code=400,
                detail="Only JPEG, PNG, and GIF images are allowed."
            )

        file_extension = Path(form.photo.filename).suffix
        unique_name = f"{int(datetime.now(timezone.utc).timestamp())}"
        unique_name += f"{file_extension}"
        file_path = ORG_PHOTOS_DIR / unique_name

        with file_path.open("wb") as buffer:
            shutil.copyfileobj(form.photo.file, buffer)

        photo_url = f"/api/static/organizations/{unique_name}"

    current_time = datetime.now(timezone.utc)
    org_id = db.organizations.insert_one(
        {
            "organization_name": form.organization_name,
            "email_domain": form.email_domain,
            "location": form.location,
            "photo_url": photo_url,
            "users": [],
            "messages": [],
            "_banned_users": [],
            "_created_at": current_time,
            "_updated_at": current_time,
        }
    )
    return {"message": "Organization added successfully",
            "organization_id": str(org_id.inserted_id)}


@app.get("/organizations", tags=["Organizations"])
def get_all_organization() -> List[Organization]:
    """route to get all Organizations"""

    db = get_engine_db()
    orgs_data = db.organizations.find()

    orgs_list = []
    for org in orgs_data:
        user_count = len(org["users"])
        orgs_list.append(
            {
                "organization_id": str(org["_id"]),
                "organization_name": org["organization_name"],
                "email_domain": org["email_domain"],
                "location": org["location"],
                "photo_url": org["photo_url"],
                # "messages":org["messages"],
                "users": org["users"],
                "user_count": user_count,
            }
        )

    return orgs_list


@app.get("/organizations/{org_id}", tags=["Organizations"])
def get_organization_by_id(org_id: str) -> Organization:
    """route get Organization by name"""
    try:
        org_obj_id = ObjectId(org_id)
    except Exception as ex:
        raise HTTPException(
            status_code=401, detail="invalid org_id format"
        ) from ex

    db = get_engine_db()
    org = db.organizations.find_one({"_id": org_obj_id})
    if not org:
        raise HTTPException(status_code=404, detail="ORGANIZATION_NOT_FOUND")

    return Organization(**{
        "organization_id": str(org["_id"]),
        "organization_name": org["organization_name"],
        "email_domain": org["email_domain"],
        "location": org["location"],
        "photo_url": org["photo_url"],
        "messages": org["messages"],
        "users": org["users"],
        "user_count": len(org["users"]),
    })


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """ route for websocket connection"""
    await websocket.accept()

    db = get_engine_db()
    org_id = None
    user_id = None
    try:

        data = await websocket.receive_json()
        token = data.get("token")
        org_id = data.get("org_id")

        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            print("token done decode")
        except ExpiredSignatureError:
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
            return
        except PyJWTError:
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
            return

        user_id = payload.get("user_id")
        print(user_id)
        if not user_id:
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
            return

        user_doc = db.users.find_one({"_id": ObjectId(user_id)})
        print("db ok ?")
        if not user_doc:
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
            return

        username = user_doc.get("username")
        manager.connect(websocket, org_id)

        await websocket.send_json({"type": "connected", "status": "ok"})

        list_msges = get_organization_messages_with_users(org_id)
        history_payload = {
            "type": "history",
            "data": list_msges
        }

        await manager.send_personal_message(history_payload, websocket)

        while True:
            message_text = await websocket.receive_text()

            new_message = {
                "_id": ObjectId(),
                "sender_id": ObjectId(user_id),
                "content": message_text,
                "timestamp": datetime.now(timezone.utc)
            }

            db.organizations.update_one(
                {"_id": ObjectId(org_id)},
                {"$push": {"messages": new_message}}
            )
# this code only handle chats in orgs add support for
# saving the chat of groups and sub groups
            broadcast_data = {
                "id": str(new_message["_id"]),
                "sender_id": user_id,
                "username": username,
                "content": message_text,
                "timestamp": new_message["timestamp"].isoformat()
            }

            await manager.broadcast(broadcast_data, org_id)

    except WebSocketDisconnect:
        manager.disconnect(websocket, org_id)
    # pylint: disable=broad-exception-caught
    except Exception as e:
        print(f"Connection error: {e}")
        if org_id:
            manager.disconnect(websocket, org_id)
        if websocket.client_state.name != "DISCONNECTED":
            await websocket.close()


@app.patch("/users")
def patch_update_user(user: AuthUser, new_user: NewPatchUser):
    """Update the fields in user based on the given fields in new_user
    """
    values_to_update = new_user.model_dump(
        exclude_unset=True, exclude_none=True)
    if len(values_to_update.keys()) == 0:
        return
    db = get_engine_db()
    if "username" in values_to_update.keys():
        found = db.users.find_one({"username": values_to_update['username']})
        if found is not None:
            raise HTTPException(
                status_code=422, detail="USERNAME_ALREADY_EXIST")
    if "password" in values_to_update.keys():
        values_to_update["password"] = password_hash.hash(
            values_to_update["password"])
    db.users.update_one({"username": {"$eq": user.username}}, {
        "$set": {
            **values_to_update,
            **{"_updated_at": datetime.now(timezone.utc)}
        }
    })
