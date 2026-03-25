from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from backend.services.realtime import manager


router = APIRouter(tags=['websocket'])


@router.websocket('/ws/chat/{shop_id}')
async def chat_ws(websocket: WebSocket, shop_id: int):
    await manager.connect(shop_id, websocket)
    try:
        while True:
            data = await websocket.receive_json()
            await manager.broadcast(shop_id, {'type': 'presence', 'payload': data})
    except WebSocketDisconnect:
        manager.disconnect(shop_id, websocket)
