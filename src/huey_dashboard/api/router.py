from fastapi import APIRouter

from .endpoints import tasks, websockets

api_router = APIRouter()

api_router.include_router(tasks.router, prefix="/tasks", tags=["tasks"])
api_router.include_router(websockets.router, prefix="/updates", tags=["websockets"])
