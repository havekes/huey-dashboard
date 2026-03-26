import json
import logging
from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from huey_dashboard.api.router import api_router as router
from huey_dashboard.services.websocket_manager import WebSocketManager


@pytest.fixture
def app():
    _app = FastAPI()
    _app.include_router(router)
    manager = MagicMock()

    # Mock connect to call accept() on the websocket
    async def mock_connect(websocket):
        await websocket.accept()

    manager.connect = AsyncMock(side_effect=mock_connect)
    manager.disconnect = MagicMock()
    _app.state.huey_dashboard = {
        "huey": MagicMock(),
        "db": MagicMock(),
        "redis": MagicMock(),
        "manager": manager,
    }
    return _app


@pytest.fixture
def client(app):
    return TestClient(app)


def test_websocket_connect_and_disconnect(app, client):
    manager = app.state.huey_dashboard["manager"]

    with client.websocket_connect("/updates/") as websocket:
        # Check if connect was called
        assert manager.connect.called

        # Test simple echo
        websocket.send_text("hello")
        data = websocket.receive_text()
        assert data == "Message received: hello"

    # After exiting the context, disconnect should be called
    assert manager.disconnect.called


@pytest.mark.asyncio
async def test_websocket_manager_logging(caplog):
    caplog.set_level(logging.DEBUG)
    manager = WebSocketManager()

    # Test connect logging
    ws = AsyncMock()
    await manager.connect(ws)
    assert "WebSocket client connected. Total active connections: 1" in caplog.text

    # Test broadcast logging
    message = {"event": "test"}
    await manager.broadcast(message)
    assert f"Broadcasting WebSocket message: {message}" in caplog.text

    # Test disconnect logging
    manager.disconnect(ws)
    assert "WebSocket client disconnected. Total active connections: 0" in caplog.text


@pytest.mark.asyncio
async def test_websocket_manager_broadcast_resiliency():
    manager = WebSocketManager()

    # Mock two websockets
    ws1 = AsyncMock()
    ws2 = AsyncMock()

    # ws1 will fail during send
    ws1.send_json.side_effect = Exception("Disconnected")

    manager.active_connections = [ws1, ws2]

    # This should not raise an exception
    await manager.broadcast({"event": "test"})

    # Both should have been attempted
    assert ws1.send_json.called
    assert ws2.send_json.called


@pytest.mark.asyncio
async def test_websocket_manager_pubsub_listener():
    manager = WebSocketManager()
    manager.broadcast = AsyncMock()  # type: ignore

    mock_redis = MagicMock()
    mock_pubsub = AsyncMock()
    mock_redis.pubsub.return_value = mock_pubsub

    # Mock listen() as an async generator
    async def mock_listen():
        yield {"type": "message", "data": json.dumps({"event": "task_enqueued"})}

    # Use MagicMock for listen so it returns the generator directly when called
    mock_pubsub.listen = MagicMock(side_effect=mock_listen)

    # Run the listener (it's an internal method)
    await manager._listen_to_pubsub(mock_redis, "test_channel")

    # Verify broadcast was called with the correct data
    assert manager.broadcast.called  # type: ignore
    assert manager.broadcast.call_args[0][0]["event"] == "task_enqueued"  # type: ignore


@pytest.mark.asyncio
async def test_websocket_manager_pubsub_malformed_json():
    manager = WebSocketManager()
    manager.broadcast = AsyncMock()  # type: ignore

    mock_redis = MagicMock()
    mock_pubsub = AsyncMock()
    mock_redis.pubsub.return_value = mock_pubsub

    async def mock_listen_malformed():
        # First one is bad
        yield {"type": "message", "data": "invalid-json"}
        # Second one is good
        yield {"type": "message", "data": json.dumps({"event": "task_finished"})}

    mock_pubsub.listen = MagicMock(side_effect=mock_listen_malformed)

    await manager._listen_to_pubsub(mock_redis, "test_channel")

    # Broadcast should have been called only once for the valid message
    assert manager.broadcast.call_count == 1  # type: ignore
    assert manager.broadcast.call_args[0][0]["event"] == "task_finished"  # type: ignore
