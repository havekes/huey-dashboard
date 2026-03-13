import asyncio
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from huey import RedisHuey
from redis.asyncio import ConnectionPool
from redis.asyncio import Redis as AsyncRedis
from sqlalchemy.ext.asyncio import AsyncEngine

from .api.router import api_router
from .services.database import TaskDatabase
from .services.signals import register_signal_handlers
from .services.websocket_manager import WebSocketManager


def init_huey_dashboard(
    app: FastAPI,
    huey: RedisHuey,
    db_engine: AsyncEngine,
    redis_pool: ConnectionPool | None = None,
    api_prefix: str = "/huey",
    bind_signals: bool = False,
) -> None:
    """
    Initialize the Huey Dashboard as a plugin for a FastAPI application.

    :param app: The host FastAPI application instance.
    :param huey: The Huey instance to monitor.
    :param db_engine: SQLAlchemy AsyncEngine instance.
    :param redis_pool: Optional Redis connection pool for async client.
    :param api_prefix: The URL prefix for the dashboard API.
    :param bind_signals: Whether to bind to Huey signals for real-time updates.
    """
    manager = WebSocketManager()
    db = TaskDatabase(db_engine)

    # Create our own async redis connection from the pool if provided
    async_redis: AsyncRedis | None = (
        AsyncRedis(connection_pool=redis_pool) if redis_pool else None
    )

    # Store state on the app
    app.state.huey_dashboard = {
        "huey": huey,
        "redis": async_redis,
        "manager": manager,
        "db": db,
        "loop": None,
    }

    # Include the dashboard router
    app.include_router(api_router, prefix=api_prefix)

    # Lifespan wrapper to handle startup/shutdown
    original_lifespan = app.router.lifespan_context

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncIterator[None]:
        # Startup logic: ensure tables exist
        await db.ensure_table()

        # Capture and store the main event loop for signal handling
        app.state.huey_dashboard["loop"] = asyncio.get_running_loop()

        if async_redis:
            await manager.start_pubsub_listener(async_redis)

        try:
            async with original_lifespan(app):
                yield
        finally:
            # Shutdown logic
            await manager.stop_pubsub_listener()
            if async_redis:
                await async_redis.aclose()

    app.router.lifespan_context = lifespan

    if bind_signals:
        # Pass the app to allow signals to dispatch back to the main loop
        register_signal_handlers(huey, db, async_redis, app=app)


__all__ = ["init_huey_dashboard"]
