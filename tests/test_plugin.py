from unittest.mock import MagicMock

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from huey import RedisHuey

from huey_dashboard import init_huey_dashboard


@pytest.fixture
def mock_db():
    conn = MagicMock()
    cur = MagicMock()
    conn.cursor.return_value.__enter__.return_value = cur
    return conn


@pytest.fixture
def mock_huey():
    huey = MagicMock(spec=RedisHuey)
    huey.pending.return_value = []
    huey.scheduled.return_value = []
    return huey


def test_plugin_init_default_prefix(mock_huey, mock_db):
    app = FastAPI()
    # Mock return value for get_all_tasks
    cur = mock_db.cursor.return_value.__enter__.return_value
    cur.fetchall.return_value = []

    init_huey_dashboard(app, huey=mock_huey, db_connection=mock_db)

    client = TestClient(app)
    # Tasks endpoint should be at /huey/tasks/
    response = client.get("/huey/tasks/")
    assert response.status_code == 200
    assert response.json() == []


def test_plugin_init_custom_prefix(mock_huey, mock_db):
    app = FastAPI()
    cur = mock_db.cursor.return_value.__enter__.return_value
    cur.fetchall.return_value = []

    init_huey_dashboard(
        app, huey=mock_huey, db_connection=mock_db, api_prefix="/admin/huey"
    )

    client = TestClient(app)
    # Check that default prefix fails
    response = client.get("/huey/tasks/")
    assert response.status_code == 404

    # Check custom prefix works
    response = client.get("/admin/huey/tasks/")
    assert response.status_code == 200


def test_plugin_state_storage(mock_huey, mock_db):
    app = FastAPI()
    mock_redis = MagicMock()
    init_huey_dashboard(app, huey=mock_huey, db_connection=mock_db, redis=mock_redis)

    assert hasattr(app.state, "huey_dashboard")
    assert app.state.huey_dashboard["huey"] == mock_huey
    assert app.state.huey_dashboard["redis"] == mock_redis
    assert "manager" in app.state.huey_dashboard
    assert "db" in app.state.huey_dashboard


def test_plugin_websocket_endpoint(mock_huey, mock_db):
    app = FastAPI()
    init_huey_dashboard(app, huey=mock_huey, db_connection=mock_db, api_prefix="/huey")

    client = TestClient(app)
    with client.websocket_connect("/huey/updates/"):
        # Note: Current websocket echo implementation in websockets.py might still exist
        # We are just testing connection here.
        pass
