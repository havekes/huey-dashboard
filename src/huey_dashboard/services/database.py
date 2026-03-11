import json
from datetime import datetime, timezone
from typing import Any, Optional, Protocol, Sequence, TypeVar

from pydantic import BaseModel

from ..models.task import TaskInfo


class Database(Protocol):
    def execute(self, query: str, params: Optional[tuple[Any, ...]] = None) -> Any: ...
    def fetchone(self, query: str, params: Optional[tuple[Any, ...]] = None) -> Any: ...
    def fetchall(self, query: str, params: Optional[tuple[Any, ...]] = None) -> Any: ...
    def commit(self) -> None: ...


class TaskRecord(BaseModel):
    id: str
    name: str
    status: str
    args: Optional[str] = None
    kwargs: Optional[str] = None
    result: Optional[str] = None
    error: Optional[str] = None
    timestamp: datetime


class TaskDatabase:
    def __init__(self, db_connection: Any):
        """
        :param db_connection: A PostgreSQL connection object (e.g. from psycopg or asyncpg).
                              For now, we assume a synchronous DB-API 2.0 compatible connection
                              provided by the host application.
        """
        self.conn = db_connection
        self._ensure_table()

    def _ensure_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS huey_tasks (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            status TEXT NOT NULL,
            args TEXT,
            kwargs TEXT,
            result TEXT,
            error TEXT,
            timestamp TIMESTAMPTZ NOT NULL
        );
        """
        with self.conn.cursor() as cur:
            cur.execute(query)
        self.conn.commit()

    def upsert_task(self, task_info: TaskInfo):
        query = """
        INSERT INTO huey_tasks (id, name, status, args, kwargs, result, error, timestamp)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (id) DO UPDATE SET
            status = EXCLUDED.status,
            result = EXCLUDED.result,
            error = EXCLUDED.error,
            timestamp = EXCLUDED.timestamp;
        """
        args_json = json.dumps(task_info.args) if task_info.args else None
        kwargs_json = json.dumps(task_info.kwargs) if task_info.kwargs else None
        result_json = json.dumps(task_info.result) if task_info.result is not None else None

        params = (
            task_info.id,
            task_info.name,
            task_info.status,
            args_json,
            kwargs_json,
            result_json,
            task_info.error,
            datetime.now(timezone.utc),
        )

        with self.conn.cursor() as cur:
            cur.execute(query, params)
        self.conn.commit()

    def get_all_tasks(self) -> list[TaskInfo]:
        query = "SELECT id, name, status, args, kwargs, result, error FROM huey_tasks ORDER BY timestamp DESC"
        with self.conn.cursor() as cur:
            cur.execute(query)
            rows = cur.fetchall()

        tasks = []
        for row in rows:
            tasks.append(
                TaskInfo(
                    id=row[0],
                    name=row[1],
                    status=row[2],
                    args=json.loads(row[3]) if row[3] else None,
                    kwargs=json.loads(row[4]) if row[4] else None,
                    result=json.loads(row[5]) if row[5] else None,
                    error=row[6],
                )
            )
        return tasks

    def get_task(self, task_id: str) -> Optional[TaskInfo]:
        query = "SELECT id, name, status, args, kwargs, result, error FROM huey_tasks WHERE id = %s"
        with self.conn.cursor() as cur:
            cur.execute(query, (task_id,))
            row = cur.fetchone()

        if not row:
            return None

        return TaskInfo(
            id=row[0],
            name=row[1],
            status=row[2],
            args=json.loads(row[3]) if row[3] else None,
            kwargs=json.loads(row[4]) if row[4] else None,
            result=json.loads(row[5]) if row[5] else None,
            error=row[6],
        )
