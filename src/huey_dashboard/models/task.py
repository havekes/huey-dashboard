import json
from datetime import datetime
from typing import Any

from pydantic import BaseModel, field_serializer


def _json_safe(obj: Any) -> Any:
    """Coerce arbitrary objects to JSON-safe types via ``default=str``."""
    if obj is None:
        return None
    return json.loads(json.dumps(obj, default=str))


class TaskInfo(BaseModel):
    id: str
    name: str
    status: str
    args: tuple[Any, ...] | None = None
    kwargs: dict[str, Any] | None = None
    result: Any | None = None
    error: str | None = None
    timestamp: datetime | None = None

    @field_serializer("args", "kwargs", "result", mode="plain")
    @classmethod
    def serialize_json_fields(cls, v: Any) -> Any:
        return _json_safe(v)
