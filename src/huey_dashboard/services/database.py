import asyncio
from datetime import UTC, datetime

from sqlalchemy import (
    JSON,
    Column,
    DateTime,
    MetaData,
    String,
    Table,
    select,
)
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncEngine

from ..models.task import TaskInfo

metadata = MetaData()

huey_tasks = Table(
    "huey_tasks",
    metadata,
    Column("id", String, primary_key=True),
    Column("name", String, nullable=False),
    Column("status", String, nullable=False),
    Column("args", JSON),
    Column("kwargs", JSON),
    Column("result", JSON),
    Column("error", String),
    Column("timestamp", DateTime(timezone=True), nullable=False),
)


class TaskDatabase:
    def __init__(self, engine: AsyncEngine) -> None:
        """
        :param engine: A SQLAlchemy AsyncEngine instance.
        """
        self.engine = engine
        self._table_ensured = False
        self._lock: asyncio.Lock | None = None

    async def ensure_table(self) -> None:
        if self._table_ensured:
            return

        if self._lock is None:
            self._lock = asyncio.Lock()

        async with self._lock:
            # Re-check after acquiring lock
            if self._table_ensured:
                return

            async with self.engine.begin() as conn:
                await conn.run_sync(metadata.create_all)
            self._table_ensured = True

    async def upsert_task(self, task_info: TaskInfo) -> None:
        await self.ensure_table()
        stmt = insert(huey_tasks).values(
            id=task_info.id,
            name=task_info.name,
            status=task_info.status,
            args=task_info.args,
            kwargs=task_info.kwargs,
            result=task_info.result,
            error=task_info.error,
            timestamp=datetime.now(UTC),
        )

        update_stmt = stmt.on_conflict_do_update(
            index_elements=["id"],
            set_={
                "status": stmt.excluded.status,
                "result": stmt.excluded.result,
                "error": stmt.excluded.error,
                "timestamp": stmt.excluded.timestamp,
            },
        )

        async with self.engine.begin() as conn:
            await conn.execute(update_stmt)

    async def get_all_tasks(self) -> list[TaskInfo]:
        await self.ensure_table()
        query = select(huey_tasks).order_by(huey_tasks.c.timestamp.desc())
        async with self.engine.begin() as conn:
            result = await conn.execute(query)
            rows = result.all()

        tasks = []
        for row in rows:
            tasks.append(
                TaskInfo(
                    id=row.id,
                    name=row.name,
                    status=row.status,
                    args=row.args,
                    kwargs=row.kwargs,
                    result=row.result,
                    error=row.error,
                )
            )
        return tasks

    async def get_task(self, task_id: str) -> TaskInfo | None:
        await self.ensure_table()
        query = select(huey_tasks).where(huey_tasks.c.id == task_id)
        async with self.engine.begin() as conn:
            result = await conn.execute(query)
            row = result.first()

        if not row:
            return None

        return TaskInfo(
            id=row.id,
            name=row.name,
            status=row.status,
            args=row.args,
            kwargs=row.kwargs,
            result=row.result,
            error=row.error,
        )
