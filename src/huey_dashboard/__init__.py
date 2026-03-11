from collections.abc import AsyncIterator
from typing import Any

from fastapi import FastAPI
from huey import RedisHuey
from redis import Redis
from redis.asyncio import Redis as AsyncRedis

from .api.router import api_router
from .services.database import TaskDatabase
from .services.signals import register_signal_handlers
from .services.websocket_manager import WebSocketManager


def init_huey_dashboard(
    app: FastAPI,
    huey: RedisHuey,
    db_connection: Any,
    redis: Redis | None = None,
    api_prefix: str = "/huey",
    bind_signals: bool = False,
) -> None:
    """
    Initialize the Huey Dashboard as a plugin for a FastAPI application.

    :param app: The host FastAPI application instance.
    :param huey: The Huey instance to monitor.
    :param db_connection: PostgreSQL connection object.
    :param redis: Optional Redis connection instance.
    :param api_prefix: The URL prefix for the dashboard API.
    :param bind_signals: Whether to bind to Huey signals for real-time updates.
    """
    manager = WebSocketManager()
    db = TaskDatabase(db_connection)

    # Use existing redis if it is already an async client, or we'll need to create one
    # Note: FastApi usually uses 'redis' as sync for storage,
    # but we need async for PubSub.
    # For now, let's assume 'redis' passed here might be the async client.
    async_redis: AsyncRedis | None = redis if isinstance(redis, AsyncRedis) else None

    # Store state on the app
    app.state.huey_dashboard = {
        "huey": huey,
        "redis": redis,
        "manager": manager,
        "db": db,
    }

    # Include the dashboard router
    app.include_router(api_router, prefix=api_prefix)

    # Lifespan wrapper to handle startup/shutdown without deprecated on_event
    from contextlib import asynccontextmanager

    original_lifespan = app.router.lifespan_context

    @asynccontextmanager
    async def dashboard_lifespan(app: FastAPI) -> AsyncIterator[None]:
        # Startup logic
        if async_redis:
            await manager.start_pubsub_listener(async_redis)

        try:
            async with original_lifespan(app):
                yield
        finally:
            # Shutdown logic
            await manager.stop_pubsub_listener()

    app.router.lifespan_context = dashboard_lifespan

    if bind_signals:
        # Note: Signals are typically triggered in the consumer process.
        # This will work if the FastAPI app and Huey consumer
        # share the database and redis.
        register_signal_handlers(huey, db, redis)


__all__ = ["init_huey_dashboard"]
