from typing import Any

from huey import RedisHuey

from ..models.task import TaskInfo
from .database import TaskDatabase


class HueyService:
    def __init__(self, huey: RedisHuey, db: TaskDatabase | None = None) -> None:
        self.huey = huey
        self.db = db

    def list_tasks(self) -> list[TaskInfo]:
        """
        List tracked tasks from the database.
        Falls back to Huey queue if database is not available (legacy behavior).
        """
        if self.db:
            return self.db.get_all_tasks()

        # Legacy polling-based list
        tasks = []
        for task in self.huey.pending():
            tasks.append(
                TaskInfo(
                    id=task.id,
                    name=task.name,
                    status="pending",
                    args=task.args,
                    kwargs=task.kwargs,
                )
            )
        for task in self.huey.scheduled():
            tasks.append(
                TaskInfo(
                    id=task.id,
                    name=task.name,
                    status="scheduled",
                    args=task.args,
                    kwargs=task.kwargs,
                )
            )
        return tasks

    def get_task_details(self, task_id: str) -> TaskInfo | None:
        """
        Get task details from the database.
        Falls back to Huey's result store/queue if database is not available.
        """
        if self.db:
            return self.db.get_task(task_id)

        # Legacy detail fetch
        result = self.huey.result(task_id, preserve=True)
        if result is not None:
            return TaskInfo(
                id=task_id, name="unknown (finished)", status="finished", result=result
            )

        for task in self.huey.pending():
            if task.id == task_id:
                return TaskInfo(
                    id=task.id,
                    name=task.name,
                    status="pending",
                    args=task.args,
                    kwargs=task.kwargs,
                )

        for task in self.huey.scheduled():
            if task.id == task_id:
                return TaskInfo(
                    id=task.id,
                    name=task.name,
                    status="scheduled",
                    args=task.args,
                    kwargs=task.kwargs,
                )

        return None


# Deprecated: periodic polling is replaced by event-driven signals
async def poll_huey_updates(huey: Any, manager: Any) -> None:
    pass
