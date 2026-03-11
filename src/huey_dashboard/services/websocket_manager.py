import asyncio
import json
from typing import Optional

from fastapi import WebSocket
from redis.asyncio import Redis


class WebSocketManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []
        self._pubsub_task: Optional[asyncio.Task] = None

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception:
                # Connection might be closed, disconnect handles it or we can ignore
                pass

    async def start_pubsub_listener(self, redis: Redis, channel: str = "huey_updates"):
        """
        Starts a background task that listens to Redis Pub/Sub and broadcasts
        incoming messages to all connected WebSockets.
        """
        if self._pubsub_task and not self._pubsub_task.done():
            return

        self._pubsub_task = asyncio.create_task(self._listen_to_pubsub(redis, channel))

    async def stop_pubsub_listener(self):
        if self._pubsub_task:
            self._pubsub_task.cancel()
            try:
                await self._pubsub_task
            except asyncio.CancelledError:
                pass

    async def _listen_to_pubsub(self, redis: Redis, channel: str):
        pubsub = redis.pubsub()
        await pubsub.subscribe(channel)

        try:
            async for message in pubsub.listen():
                if message["type"] == "message":
                    try:
                        data = json.loads(message["data"])
                        await self.broadcast(data)
                    except (json.JSONDecodeError, TypeError):
                        # Log error in a real app
                        pass
        finally:
            await pubsub.unsubscribe(channel)
            await pubsub.close()
