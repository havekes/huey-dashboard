from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from huey import RedisHuey

from huey_dashboard import init_huey_dashboard


@pytest.fixture
def mock_db_engine():
    engine = MagicMock()
    conn = AsyncMock()

    # Mock result of conn.execute
    result = MagicMock()
    result.all.return_value = []
    result.first.return_value = None
    conn.execute.return_value = result

    # Mock engine.begin() and engine.connect() to return our mocked connection
    engine.begin.return_value.__aenter__.return_value = conn
    engine.connect.return_value.__aenter__.return_value = conn

    return engine


@pytest.fixture
def mock_huey():
    huey = MagicMock(spec=RedisHuey)
    huey.pending.return_value = []
    huey.scheduled.return_value = []
    return huey


@pytest.fixture
def mock_redis_pool():
    return MagicMock()


@pytest.mark.asyncio
async def test_plugin_init_default_prefix(mock_huey, mock_db_engine):
    app = FastAPI()
    init_huey_dashboard(app, huey=mock_huey, db_engine=mock_db_engine)

    client = TestClient(app)
    response = client.get("/huey/tasks/")
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_plugin_init_custom_prefix(mock_huey, mock_db_engine):
    app = FastAPI()
    init_huey_dashboard(
        app, huey=mock_huey, db_engine=mock_db_engine, api_prefix="/admin/huey"
    )

    client = TestClient(app)
    # Check that default prefix fails
    response = client.get("/huey/tasks/")
    assert response.status_code == 404

    # Check custom prefix works
    response = client.get("/admin/huey/tasks/")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_plugin_state_storage(mock_huey, mock_db_engine, mock_redis_pool):
    app = FastAPI()
    init_huey_dashboard(
        app,
        huey=mock_huey,
        db_engine=mock_db_engine,
        redis_pool=mock_redis_pool,
    )

    assert hasattr(app.state, "huey_dashboard")
    assert app.state.huey_dashboard["huey"] == mock_huey
    assert "manager" in app.state.huey_dashboard
    assert "db" in app.state.huey_dashboard
    assert app.state.huey_dashboard["redis"] is not None


@pytest.mark.asyncio
async def test_plugin_websocket_endpoint(mock_huey, mock_db_engine):
    app = FastAPI()
    init_huey_dashboard(
        app, huey=mock_huey, db_engine=mock_db_engine, api_prefix="/huey"
    )

    client = TestClient(app)
    with client.websocket_connect("/huey/updates/"):
        pass
