import asyncio
import json
import logging
import threading
from datetime import UTC, datetime
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

logger = logging.getLogger(__name__)


class _BackgroundLoop:
    """Manages a dedicated asyncio event loop on a background thread.

    Used by signal handlers that run in synchronous contexts (e.g. Huey
    worker processes) where no event loop is available.
    """

    _loop: asyncio.AbstractEventLoop | None = None
    _thread: threading.Thread | None = None
    _lock = threading.Lock()

    @classmethod
    def get(cls) -> asyncio.AbstractEventLoop:
        with cls._lock:
            if cls._loop is None or cls._thread is None or not cls._thread.is_alive():
                cls._loop = asyncio.new_event_loop()
                cls._thread = threading.Thread(
                    target=cls._loop.run_forever, daemon=True
                )
                cls._thread.start()
            return cls._loop


def register_signal_handlers(
    huey: RedisHuey,
    db: TaskDatabase,
    redis: Redis | None = None,
    loop: asyncio.AbstractEventLoop | None = None,
) -> None:
    """Register signal handlers for Huey task lifecycle events.

    When an event occurs, we update the task state in the database
    and publish a message to Redis Pub/Sub for the dashboard to pick up.

    Args:
        huey: The Huey instance to attach signal handlers to.
        db: The TaskDatabase used to persist task state.
        redis: Optional async Redis client for pub/sub broadcasting.
        loop: An explicit event loop to schedule work on (e.g. the
            FastAPI main loop). If *None*, a background loop is used.
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
        status = signal.replace("huey.signal.", "").lower()
        logger.info(
            "Received Huey signal: %s (status=%s) for task: %s",
            signal,
            status,
            task.id,
        )

        task_info = TaskInfo(
            id=task.id,
            name=task.name,
            status=status,
            args=task.args,
            kwargs=task.kwargs,
            error=str(exc) if exc else None,
            timestamp=datetime.now(UTC),
        )

        async def _persist() -> None:
            try:
                await db.upsert_task(task_info)
                logger.debug("Upserted task %s with status %s", task.id, status)

                if redis:
                    event_data = {
                        "event": f"task_{status}",
                        "task": task_info.model_dump(mode="json"),
                    }
                    await redis.publish("huey_updates", json.dumps(event_data))
                    logger.debug(
                        "Published %s update for task %s to Redis",
                        status,
                        task.id,
                    )
            except Exception:
                logger.exception(
                    "Error handling signal %s for task %s", signal, task.id
                )

        # Pick an event loop to schedule the async work on.
        target_loop = loop
        if target_loop is None:
            try:
                target_loop = asyncio.get_running_loop()
            except RuntimeError:
                target_loop = None

        if target_loop is not None and target_loop.is_running():
            target_loop.call_soon_threadsafe(_create_task, target_loop, _persist())
        else:
            # No running loop available (typical for Huey worker processes).
            bg = _BackgroundLoop.get()
            bg.call_soon_threadsafe(_create_task, bg, _persist())


def _create_task(loop: asyncio.AbstractEventLoop, coro: Any) -> None:
    """Create a task on *loop* and prevent it from being garbage-collected."""
    task = loop.create_task(coro)
    # prevent GC before completion
    task.add_done_callback(lambda t: None)
