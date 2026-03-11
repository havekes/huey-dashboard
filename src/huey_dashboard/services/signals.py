import json
from typing import Any, Optional

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
from redis import Redis

from ..models.task import TaskInfo
from .database import TaskDatabase


def register_signal_handlers(
    huey: RedisHuey, db: TaskDatabase, redis: Optional[Redis] = None
):
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
    def handle_task_event(signal: str, task: Any, exc: Optional[Exception] = None):
        # Map signal to status
        status = signal.replace("huey.signal.", "").lower()

        task_info = TaskInfo(
            id=task.id,
            name=task.name,
            status=status,
            args=task.args,
            kwargs=task.kwargs,
            error=str(exc) if exc else None,
            # For SIGNAL_COMPLETE, we might need to fetch the result separately
            # but usually 'task' object in SIGNAL_COMPLETE doesn't have the result yet.
            # We can handle result specifically if needed.
        )

        # 1. Persist to PostgreSQL
        db.upsert_task(task_info)

        # 2. Publish to Redis Pub/Sub for real-time WebSocket updates
        if redis:
            event_data = {
                "event": f"task_{status}",
                "task": task_info.model_dump(),
            }
            try:
                redis.publish("huey_updates", json.dumps(event_data))
            except Exception:
                # Log error in a real app
                pass
