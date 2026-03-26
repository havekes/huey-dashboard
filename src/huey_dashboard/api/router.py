import logging

from fastapi import APIRouter, Depends, Request, WebSocket

from .endpoints import tasks, websockets

logger = logging.getLogger(__name__)


async def log_request(request: Request) -> None:
    """
    Dependency to log incoming dashboard API requests.
    """
    logger.debug("Dashboard API request: %s %s", request.method, request.url.path)


async def log_websocket(websocket: WebSocket) -> None:
    """
    Dependency to log incoming dashboard WebSocket connections.
    """
    logger.debug("Dashboard WebSocket connection: %s", websocket.url.path)


api_router = APIRouter()

api_router.include_router(
    tasks.router,
    prefix="/tasks",
    tags=["tasks"],
    dependencies=[Depends(log_request)],
)
api_router.include_router(
    websockets.router,
    prefix="/updates",
    tags=["websockets"],
    dependencies=[Depends(log_websocket)],
)
