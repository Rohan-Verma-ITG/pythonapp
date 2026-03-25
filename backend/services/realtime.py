from collections import defaultdict
from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        self.connections: dict[int, list[WebSocket]] = defaultdict(list)

    async def connect(self, shop_id: int, websocket: WebSocket):
        await websocket.accept()
        self.connections[shop_id].append(websocket)

    def disconnect(self, shop_id: int, websocket: WebSocket):
        if websocket in self.connections.get(shop_id, []):
            self.connections[shop_id].remove(websocket)

    async def broadcast(self, shop_id: int, payload: dict):
        for ws in list(self.connections.get(shop_id, [])):
            await ws.send_json(payload)


manager = ConnectionManager()
