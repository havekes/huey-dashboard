from huey import RedisHuey
from redis import Redis
from starlette.requests import HTTPConnection

from ..services.database import TaskDatabase
from ..services.websocket_manager import WebSocketManager


def get_redis_client(conn: HTTPConnection) -> Redis:
    return conn.app.state.huey_dashboard["redis"]


def get_huey_client(conn: HTTPConnection) -> RedisHuey:
    return conn.app.state.huey_dashboard["huey"]


def get_websocket_manager(conn: HTTPConnection) -> WebSocketManager:
    return conn.app.state.huey_dashboard["manager"]


def get_task_db(conn: HTTPConnection) -> TaskDatabase:
    return conn.app.state.huey_dashboard["db"]
