import logging
from unittest.mock import AsyncMock, MagicMock

import pytest

from huey_dashboard.models.task import TaskInfo
from huey_dashboard.services.database import TaskDatabase


@pytest.fixture
def mock_engine():
    engine = MagicMock()
    # Mock engine.begin() as an async context manager
    conn = AsyncMock()
    engine.begin.return_value.__aenter__.return_value = conn
    # Mock engine.connect() as an async context manager
    engine.connect.return_value.__aenter__.return_value = conn
    return engine, conn


@pytest.mark.asyncio
async def test_upsert_task(mock_engine, caplog):
    caplog.set_level(logging.DEBUG)
    engine, conn = mock_engine
    db = TaskDatabase(engine)
    task = TaskInfo(id="test-id", name="test-task", status="enqueued")

    await db.upsert_task(task)

    # Check if execute was called on the connection
    assert conn.execute.call_count == 1

    # Verify log emission
    assert f"Upserted task: {task.id} with status: {task.status}" in caplog.text


@pytest.mark.asyncio
async def test_get_all_tasks(mock_engine):
    engine, conn = mock_engine
    db = TaskDatabase(engine)

    # Mock result.all()
    result = MagicMock()
    row = MagicMock()
    row.id = "id1"
    row.name = "name1"
    row.status = "status1"
    row.args = None
    row.kwargs = None
    row.result = None
    row.error = None
    result.all.return_value = [row]
    conn.execute.return_value = result

    tasks = await db.get_all_tasks()

    assert len(tasks) == 1
    assert tasks[0].id == "id1"
