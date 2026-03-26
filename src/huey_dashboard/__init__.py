import asyncio
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from huey import RedisHuey
from redis.asyncio import Redis as AsyncRedis
from sqlalchemy.ext.asyncio import create_async_engine

from .api.router import api_router
from .services.database import TaskDatabase
from .services.signals import register_signal_handlers
from .services.websocket_manager import WebSocketManager


def init_huey_dashboard(
    app: FastAPI,
    huey: RedisHuey,
    db_url: str,
    redis_url: str | None = None,
    api_prefix: str = "/huey",
    bind_signals: bool = False,
) -> None:
    """Initialize the Huey Dashboard as a plugin for a FastAPI application.

    This sets up the REST + WebSocket API for monitoring Huey tasks and,
    optionally, registers signal handlers so that the *API process* can
    track task events that originate here (e.g. ``SIGNAL_ENQUEUED``).

    .. note::

        Signals like ``EXECUTING`` and ``COMPLETE`` fire in the **worker
        process**, not the API process.  To capture those you must also
        call :func:`init_worker_signals` in your Huey task module so that
        the worker has its own signal handlers.

    Args:
        app: The host FastAPI application instance.
        huey: The Huey instance to monitor.
        db_url: SQLAlchemy-style async database URL.
        redis_url: Optional Redis URL for pub/sub broadcasting.
        api_prefix: URL prefix for the dashboard API.
        bind_signals: Whether to bind signal handlers in this process.
    """
    engine = create_async_engine(db_url)
    db = TaskDatabase(engine)
    manager = WebSocketManager()

    async_redis: AsyncRedis | None = None
    if redis_url:
        async_redis = AsyncRedis.from_url(redis_url)

    # Store state on the app for dependency injection
    app.state.huey_dashboard = {
        "huey": huey,
        "redis": async_redis,
        "manager": manager,
        "db": db,
    }

    app.include_router(api_router, prefix=api_prefix)

    original_lifespan = app.router.lifespan_context

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncIterator[None]:
        await db.ensure_table()

        main_loop = asyncio.get_running_loop()

        if bind_signals:
            # Pass the main event loop so signal callbacks are scheduled on
            # the loop that owns the async DB engine.
            register_signal_handlers(huey, db, async_redis, loop=main_loop)

        if async_redis:
            await manager.start_pubsub_listener(async_redis)

        try:
            async with original_lifespan(app) as state:
                yield state
        finally:
            await manager.stop_pubsub_listener()
            if async_redis:
                await async_redis.aclose()

    app.router.lifespan_context = lifespan


def init_worker_signals(
    huey: RedisHuey,
    db_url: str,
    redis_url: str | None = None,
) -> None:
    """Register signal handlers for a Huey **worker** process.

    Call this at module level in the file where your Huey instance and
    tasks are defined.  When the Huey consumer imports that module it
    will register the handlers on the worker's own ``Huey`` instance,
    allowing lifecycle signals (``executing``, ``complete``, ``error``,
    etc.) to be persisted to the database and broadcast via Redis.

    Example usage::

        # tasks.py
        from huey import RedisHuey
        from huey_dashboard import init_worker_signals

        huey = RedisHuey("my-app", url="redis://localhost:6379/0")
        init_worker_signals(
            huey,
            db_url="postgresql+asyncpg://user:pass@localhost/mydb",
            redis_url="redis://localhost:6379/0",
        )

        @huey.task()
        def my_task(x, y):
            return x + y

    Args:
        huey: The Huey instance used by the worker.
        db_url: SQLAlchemy-style async database URL.
        redis_url: Optional Redis URL for pub/sub broadcasting.
    """
    engine = create_async_engine(db_url)
    db = TaskDatabase(engine)

    redis: AsyncRedis | None = None
    if redis_url:
        redis = AsyncRedis.from_url(redis_url)

    # No explicit loop — the background-loop fallback in
    # register_signal_handlers will be used automatically since
    # worker processes don't have a running asyncio loop.
    register_signal_handlers(huey, db, redis)


__all__ = ["init_huey_dashboard", "init_worker_signals"]
