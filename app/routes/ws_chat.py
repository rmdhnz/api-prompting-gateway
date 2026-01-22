from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.core.ws_manager import manager

router = APIRouter()

@router.websocket("/ws/chat/{baus_user_id}")
async def chat_ws(websocket: WebSocket, 
baus_user_id: int):
    print("🟢 WS CONNECT:", baus_user_id)
    await manager.connect(baus_user_id, websocket)
    try:
        while True:
            await websocket.receive_text() 
    except WebSocketDisconnect:
        manager.disconnect(baus_user_id, websocket)

