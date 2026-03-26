import asyncio
import json
import logging
from unittest.mock import AsyncMock, MagicMock

import pytest

from huey_dashboard.services.signals import register_signal_handlers


@pytest.fixture
def mock_huey_and_handler():
    huey = MagicMock()
    handler_fn = None

    def mock_signal_decorator(*args, **kwargs):
        def wrapper(fn):
            nonlocal handler_fn
            handler_fn = fn
            return fn

        return wrapper

    huey.signal = mock_signal_decorator
    return huey, lambda: handler_fn


@pytest.mark.parametrize(
    "signal,expected_status",
    [
        ("huey.signal.ENQUEUED", "enqueued"),
        ("huey.signal.EXECUTING", "executing"),
        ("huey.signal.COMPLETE", "complete"),
        ("huey.signal.ERROR", "error"),
        ("huey.signal.REVOKED", "revoked"),
        ("huey.signal.RETRYING", "retrying"),
        ("huey.signal.INTERRUPTED", "interrupted"),
    ],
)
@pytest.mark.asyncio
async def test_signal_handler_various_signals(
    mock_huey_and_handler, signal, expected_status, caplog
):
    caplog.set_level(logging.DEBUG)
    huey, get_handler = mock_huey_and_handler
    db = MagicMock()
    db.upsert_task = AsyncMock()
    db.ensure_table = AsyncMock()
    redis = MagicMock()
    redis.publish = AsyncMock()

    # Pass the current running loop explicitly so the handler schedules
    # work on this loop (rather than creating a background thread).
    loop = asyncio.get_running_loop()
    register_signal_handlers(huey, db, redis, loop=loop)
    handler_fn = get_handler()

    task = MagicMock()
    task.id = f"test-id-{expected_status}"
    task.name = "test-task"
    task.args = (1, 2)
    task.kwargs = {"a": 3}

    exc = Exception("test error") if expected_status == "error" else None
    handler_fn(signal, task, exc=exc)

    # Give the scheduled coroutine time to run
    await asyncio.sleep(0.1)

    # Verify log emission
    assert (
        f"Received Huey signal: {signal} (status={expected_status}) for task: {task.id}"
        in caplog.text
    )

    # Verify DB upsert
    assert db.upsert_task.call_count == 1
    task_info = db.upsert_task.call_args[0][0]
    assert task_info.id == task.id
    assert task_info.status == expected_status
    if expected_status == "error":
        assert task_info.error == "test error"

    # Verify Redis publish
    assert redis.publish.call_count == 1
    channel, message = redis.publish.call_args[0]
    assert channel == "huey_updates"
    data = json.loads(message)
    assert data["event"] == f"task_{expected_status}"
    assert data["task"]["id"] == task.id


@pytest.mark.asyncio
async def test_signal_handler_redis_failure_graceful(mock_huey_and_handler):
    huey, get_handler = mock_huey_and_handler
    db = MagicMock()
    db.upsert_task = AsyncMock()
    db.ensure_table = AsyncMock()
    redis = MagicMock()
    redis.publish = AsyncMock(side_effect=Exception("Redis connection lost"))

    loop = asyncio.get_running_loop()
    register_signal_handlers(huey, db, redis, loop=loop)
    handler_fn = get_handler()

    task = MagicMock()
    task.id = "test-id-redis-fail"
    task.name = "test-task"
    task.args = ()
    task.kwargs = {}

    # This should not raise an exception
    handler_fn("huey.signal.ENQUEUED", task)

    await asyncio.sleep(0.1)

    # DB should still have been updated
    assert db.upsert_task.call_count == 1
    # Redis publish was attempted
    assert redis.publish.call_count == 1
