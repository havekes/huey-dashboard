import asyncio
import json
from typing import Any

from huey import RedisHuey
from huey.signals import (
    SIGNAL_COMPLETE,
    SIGNAL_ENQUEUED,
    SIGNAL_ERROR,
    SIGNAL_EXECUTING,
    SIGNAL_INTERRUPTED,
    SIGNAL_RETRYING,
    SIGNAL_REVOKED,
    SIGNAL_SCHEDULED,
)
from redis.asyncio import Redis

from ..models.task import TaskInfo
from .database import TaskDatabase


def register_signal_handlers(
    huey: RedisHuey,
    db: TaskDatabase,
    redis: Redis | None = None,
    app: Any = None,
) -> None:
    """
    Register signal handlers for Huey task lifecycle events.
    When an event occurs, we update the task state in the database
    and publish a message to Redis Pub/Sub for the dashboard to pick up.
    """

    @huey.signal(
        SIGNAL_ENQUEUED,
        SIGNAL_SCHEDULED,
        SIGNAL_EXECUTING,
        SIGNAL_COMPLETE,
        SIGNAL_ERROR,
        SIGNAL_RETRYING,
        SIGNAL_REVOKED,
        SIGNAL_INTERRUPTED,
    )
    def handle_task_event(signal: str, task: Any, exc: Exception | None = None) -> None:
        # Map signal to status
        status = signal.replace("huey.signal.", "").lower()

        task_info = TaskInfo(
            id=task.id,
            name=task.name,
            status=status,
            args=task.args,
            kwargs=task.kwargs,
            error=str(exc) if exc else None,
        )

        async def _handle():
            # 1. Persist to PostgreSQL
            await db.upsert_task(task_info)

            # 2. Publish to Redis Pub/Sub for real-time WebSocket updates
            if redis:
                event_data = {
                    "event": f"task_{status}",
                    "task": task_info.model_dump(),
                }
                try:
                    await redis.publish("huey_updates", json.dumps(event_data))
                except Exception:
                    # Log error in a real app
                    pass

        # Dispatch the async handler
        main_loop = None
        if app and hasattr(app, "state") and hasattr(app.state, "huey_dashboard"):
            main_loop = app.state.huey_dashboard.get("loop")

        if main_loop and main_loop.is_running():
            # Schedule on the main loop from any thread
            main_loop.call_soon_threadsafe(lambda: asyncio.create_task(_handle()))
        else:
            # Fallback for when the main loop is not available in this process/context
            try:
                loop = asyncio.get_running_loop()
                loop.create_task(_handle())
            except RuntimeError:
                # No running loop in this thread, run it to completion
                asyncio.run(_handle())
