from typing import Any

from pydantic import BaseModel


class TaskInfo(BaseModel):
    id: str
    name: str
    status: str
    args: tuple | None = None
    kwargs: dict | None = None
    result: Any | None = None
    error: str | None = None
