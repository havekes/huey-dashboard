import json
from unittest.mock import MagicMock

from huey_dashboard.services.signals import register_signal_handlers


def test_signal_handler_persists_to_db():
    huey = MagicMock()
    db = MagicMock()
    redis = MagicMock()

    # Capture the registered signal handler
    handler_fn = None

    def mock_signal_decorator(*args, **kwargs):
        def wrapper(fn):
            nonlocal handler_fn
            handler_fn = fn
            return fn

        return wrapper

    huey.signal = mock_signal_decorator

    register_signal_handlers(huey, db, redis)

    assert handler_fn is not None

    # Simulate a signal
    task = MagicMock()
    task.id = "test-id"
    task.name = "test-task"
    task.args = (1, 2)
    task.kwargs = {"a": 3}

    handler_fn("huey.signal.ENQUEUED", task)

    # Verify DB upsert
    assert db.upsert_task.call_count == 1
    task_info = db.upsert_task.call_args[0][0]
    assert task_info.id == "test-id"
    assert task_info.status == "enqueued"

    # Verify Redis publish
    assert redis.publish.call_count == 1
    channel, message = redis.publish.call_args[0]
    assert channel == "huey_updates"
    data = json.loads(message)
    assert data["event"] == "task_enqueued"
    assert data["task"]["id"] == "test-id"
