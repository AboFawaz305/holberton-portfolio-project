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

chat = APIRouter(prefix="/ws/chat", tags=["chat"])
manager = ConnectionManager()


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


@chat.websocket("")
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
