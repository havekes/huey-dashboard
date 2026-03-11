from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect

from ...core.dependencies import get_websocket_manager
from ...services.websocket_manager import WebSocketManager

router = APIRouter()


@router.websocket("/")
async def websocket_endpoint(
    websocket: WebSocket, manager: WebSocketManager = Depends(get_websocket_manager)
):
    await manager.connect(websocket)
    try:
        while True:
            # We don't expect messages from the client for now,
            # but we need to keep the connection open.
            data = await websocket.receive_text()
            # Simple echo for testing
            await websocket.send_text(f"Message received: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
