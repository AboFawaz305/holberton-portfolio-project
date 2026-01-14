"""Chat websocket definition
"""
from datetime import datetime, timezone

import jwt
from bson.objectid import ObjectId
from constants import ALGORITHM, SECRET_KEY
from core.ConnectionManager import ConnectionManager
from db import get_engine_db
from fastapi import status
from fastapi.routing import APIRouter
from fastapi.websockets import WebSocket, WebSocketDisconnect
from jwt.exceptions import ExpiredSignatureError, PyJWTError
from spam_model import is_spam

chat = APIRouter(prefix="/ws/chat", tags=["chat"])
manager = ConnectionManager()


def get_messages_with_users(room_id: str, is_org: bool):
    """Gets messages with user info for org or group"""
    db = get_engine_db()

    collection = db. organizations if is_org else db.groups

    pipeline = [
        {"$match": {"_id": ObjectId(room_id)}},
        {"$unwind": {"path": "$messages",
                     "preserveNullAndEmptyArrays": False}},
        {
            "$lookup": {
                "from": "users",
                "localField": "messages.sender_id",
                "foreignField":  "_id",
                "as":  "sender_info"
            }
        },
        {"$unwind": {"path": "$sender_info",
                     "preserveNullAndEmptyArrays": True}},
        {
            "$project": {
                "_id": 0,
                "message_id": {"$toString": "$messages._id"},
                "content": "$messages.content",
                "timestamp": {
                    "$dateToString": {
                        "format": "%Y-%m-%dT%H:%M:%S.%LZ",  # ← Remove space
                        "date": "$messages.timestamp",
                        "timezone":  "UTC"
                    }
                },
                "user": {
                    "_id": {"$toString":  "$sender_info._id"},
                    "username":  "$sender_info.username",
                }
            }
        }
    ]

    return list(collection.aggregate(pipeline))


def save_message_to_db(room_id: str, is_org:  bool, message: dict):
    """Saves a message to the appropriate collection"""
    db = get_engine_db()
    collection = db.organizations if is_org else db.groups

    collection.update_one(
        {"_id": ObjectId(room_id)},
        {"$push": {"messages": message}}
    )


# pylint: disable=too-many-locals
@chat.websocket("")
async def websocket_endpoint(websocket: WebSocket):
    """ route for websocket connection"""
    await websocket.accept()

    db = get_engine_db()
    room_id = None
    is_org = True
    user_id = None

    try:

        data = await websocket.receive_json()
        token = data.get("token")
        room_id = data.get("room_id")
        is_org = data.get("isOrg", True)

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
        manager.connect(websocket, room_id)

        await websocket.send_json({"type": "connected", "status": "ok"})

        list_msges = get_messages_with_users(room_id, is_org)
        history_payload = {
            "type": "history",
            "data": list_msges
        }

        await manager.send_personal_message(history_payload, websocket)

        while True:
            message_text = await websocket.receive_text()
            if is_spam(message_text):
                await manager.send_personal_message({
                    "error": "MESSAGE_IS_SPAM"
                }, websocket)
                continue

            new_message = {
                "_id": ObjectId(),
                "sender_id": ObjectId(user_id),
                "content": message_text,
                "timestamp": datetime.now(timezone.utc)
            }

            save_message_to_db(room_id, is_org, new_message)

            broadcast_data = {
                "id": str(new_message["_id"]),
                "sender_id": user_id,
                "username": username,
                "content": message_text,
                "timestamp": new_message["timestamp"].isoformat()
            }

            await manager.broadcast(broadcast_data, room_id)

    except WebSocketDisconnect:
        manager.disconnect(websocket, room_id)
    # pylint: disable=broad-exception-caught
    except Exception as e:
        print(f"Connection error: {e}")
        if room_id:
            manager.disconnect(websocket, room_id)
        if websocket.client_state.name != "DISCONNECTED":
            await websocket.close()
