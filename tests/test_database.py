from unittest.mock import MagicMock

import pytest
from huey_dashboard.models.task import TaskInfo
from huey_dashboard.services.database import TaskDatabase


@pytest.fixture
def mock_conn():
    conn = MagicMock()
    # Mock the cursor context manager
    cur = MagicMock()
    conn.cursor.return_value.__enter__.return_value = cur
    return conn


def test_upsert_task(mock_conn):
    db = TaskDatabase(mock_conn)
    task = TaskInfo(id="test-id", name="test-task", status="enqueued")

    db.upsert_task(task)

    cur = mock_conn.cursor.return_value.__enter__.return_value
    # Check if execute was called (ignoring table creation in __init__)
    # We can check the second call to execute which is the upsert
    assert cur.execute.call_count >= 2
    args, _ = cur.execute.call_args
    assert "INSERT INTO huey_tasks" in args[0]
    assert args[1][0] == "test-id"
    assert args[1][2] == "enqueued"


def test_get_all_tasks(mock_conn):
    db = TaskDatabase(mock_conn)
    cur = mock_conn.cursor.return_value.__enter__.return_value
    cur.fetchall.return_value = [
        ("id1", "name1", "status1", None, None, None, None),
        ("id2", "name2", "status2", None, None, None, None),
    ]

    tasks = db.get_all_tasks()

    assert len(tasks) == 2
    assert tasks[0].id == "id1"
    assert tasks[1].id == "id2"
