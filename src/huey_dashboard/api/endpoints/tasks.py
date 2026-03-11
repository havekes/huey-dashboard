from typing import Any

from fastapi import APIRouter, Depends, HTTPException

from ...core.dependencies import get_huey_client, get_task_db
from ...models.task import TaskInfo
from ...services.database import TaskDatabase
from ...services.huey_service import HueyService

router = APIRouter()


def get_huey_service(
    huey: Any = Depends(get_huey_client), db: TaskDatabase = Depends(get_task_db)
) -> HueyService:
    return HueyService(huey, db)


@router.get("/", response_model=list[TaskInfo])
async def list_tasks(
    service: HueyService = Depends(get_huey_service),
) -> list[TaskInfo]:
    return service.list_tasks()


@router.get("/{task_id}", response_model=TaskInfo)
async def get_task(
    task_id: str, service: HueyService = Depends(get_huey_service)
) -> TaskInfo:
    task = service.get_task_details(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task
