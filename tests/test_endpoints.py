from unittest.mock import MagicMock

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from huey_dashboard.api.router import api_router as router
from huey_dashboard.models.task import TaskInfo


@pytest.fixture
def app():
    _app = FastAPI()
    _app.include_router(router)
    # Setup mock state
    _app.state.huey_dashboard = {
        "huey": MagicMock(),
        "db": MagicMock(),
        "redis": MagicMock(),
        "manager": MagicMock(),
    }
    return _app


@pytest.fixture
def client(app):
    return TestClient(app)


def test_list_tasks(app, client):
    db = app.state.huey_dashboard["db"]
    mock_tasks = [
        TaskInfo(id="1", name="task1", status="enqueued"),
        TaskInfo(id="2", name="task2", status="complete"),
    ]
    db.get_all_tasks.return_value = mock_tasks

    response = client.get("/tasks/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["id"] == "1"
    assert data[1]["id"] == "2"


def test_get_task_success(app, client):
    db = app.state.huey_dashboard["db"]
    mock_task = TaskInfo(id="1", name="task1", status="enqueued")
    db.get_task.return_value = mock_task

    response = client.get("/tasks/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == "1"


def test_get_task_not_found(app, client):
    db = app.state.huey_dashboard["db"]
    db.get_task.return_value = None

    response = client.get("/tasks/non-existent")
    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"


def test_list_tasks_fallback(app, client):
    # Set DB to None to trigger fallback
    app.state.huey_dashboard["db"] = None
    huey = app.state.huey_dashboard["huey"]

    task_pending = MagicMock()
    task_pending.id = "p1"
    task_pending.name = "pending-task"
    task_pending.args = ()
    task_pending.kwargs = {}

    task_scheduled = MagicMock()
    task_scheduled.id = "s1"
    task_scheduled.name = "scheduled-task"
    task_scheduled.args = ()
    task_scheduled.kwargs = {}

    huey.pending.return_value = [task_pending]
    huey.scheduled.return_value = [task_scheduled]

    response = client.get("/tasks/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    statuses = [t["status"] for t in data]
    assert "pending" in statuses
    assert "scheduled" in statuses


def test_get_task_fallback(app, client):
    app.state.huey_dashboard["db"] = None
    huey = app.state.huey_dashboard["huey"]

    # Mock result() to return None first (not finished)
    huey.result.return_value = None

    task_pending = MagicMock()
    task_pending.id = "p1"
    task_pending.name = "pending-task"
    task_pending.args = ()
    task_pending.kwargs = {}
    huey.pending.return_value = [task_pending]
    huey.scheduled.return_value = []

    response = client.get("/tasks/p1")
    assert response.status_code == 200
    assert response.json()["id"] == "p1"
    assert response.json()["status"] == "pending"


def test_get_task_fallback_finished(app, client):
    app.state.huey_dashboard["db"] = None
    huey = app.state.huey_dashboard["huey"]

    # Mock result() to return something (finished)
    huey.result.return_value = "task-result"

    response = client.get("/tasks/f1")
    assert response.status_code == 200
    assert response.json()["id"] == "f1"
    assert response.json()["status"] == "finished"
    assert response.json()["result"] == "task-result"
