"""Connections to websockets manager
"""
from fastapi.websockets import WebSocket


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
