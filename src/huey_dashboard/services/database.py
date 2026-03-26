import logging
import threading
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

logger = logging.getLogger(__name__)

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
        self._lock = threading.Lock()

    async def ensure_table(self) -> None:
        if self._table_ensured:
            return

        # Double-check with a lock to avoid redundant creation attempts across threads.
        # Note: We don't hold the threading lock across the 'await' call to avoid
        # blocking other threads' event loops unnecessarily.
        with self._lock:
            if self._table_ensured:
                return

        async with self.engine.begin() as conn:
            await conn.run_sync(metadata.create_all)

        self._table_ensured = True

    async def upsert_task(self, task_info: TaskInfo) -> None:
        await self.ensure_table()
        # Use Pydantic's model_dump(mode='json') to ensure all fields (like UUIDs)
        # are converted to JSON-serializable types.
        data = task_info.model_dump(mode="json")
        logger.debug("Upserting task data: %s", data)

        ts = task_info.timestamp or datetime.now(UTC)
        stmt = insert(huey_tasks).values(
            id=data["id"],
            name=data["name"],
            status=data["status"],
            args=data["args"],
            kwargs=data["kwargs"],
            result=data["result"],
            error=data["error"],
            timestamp=ts,
        )

        update_stmt = stmt.on_conflict_do_update(
            index_elements=["id"],
            set_={
                "status": stmt.excluded.status,
                "result": stmt.excluded.result,
                "error": stmt.excluded.error,
                "timestamp": stmt.excluded.timestamp,
            },
            where=(stmt.excluded.timestamp >= huey_tasks.c.timestamp),
        )

        async with self.engine.begin() as conn:
            result = await conn.execute(update_stmt)
            logger.info(
                "Upserted task: %s with status: %s (rowcount: %s)",
                task_info.id,
                task_info.status,
                result.rowcount,
            )

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
                    timestamp=row.timestamp,
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
            timestamp=row.timestamp,
        )
