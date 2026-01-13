"""Connections to websockets manager
"""
from fastapi.websockets import WebSocket


class ConnectionManager:
    """ manager class for websocket connections"""

    def __init__(self):
        self.active_connections: dict[str, list[WebSocket]] = {}

    def connect(self, websocket: WebSocket, room_id: str):
        """add a websocket to an org"""
        if room_id not in self.active_connections:
            self.active_connections[room_id] = []
        self.active_connections[room_id].append(websocket)

    def disconnect(self, websocket: WebSocket, room_id: str):
        """removes a websocket connection"""
        if room_id in self.active_connections:
            if websocket in self.active_connections[room_id]:
                self.active_connections[room_id].remove(websocket)
            if not self.active_connections[room_id]:
                del self.active_connections[room_id]

    async def send_personal_message(self, message, websocket: WebSocket):
        """send to self a massage"""
        await websocket.send_json(message)

    async def broadcast(self, message_payload: dict, room_id: str):
        """broadcast a massage to all websockets with same org_id"""
        if room_id in self.active_connections:
            for connection in self.active_connections[room_id]:
                await connection.send_json(message_payload)
