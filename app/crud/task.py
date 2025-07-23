import uuid
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.task import Task
from app.schemas.task import TaskCreate


async def create_task(session: AsyncSession, task_in: TaskCreate) -> Task:
    task = Task(**task_in.model_dump())
    session.add(task)
    await session.commit()
    await session.refresh(task)
    return task


async def get_task(session: AsyncSession, task_id: uuid.UUID) -> Task | None:
    result = await session.execute(select(Task).where(Task.id == task_id))
    return result.scalars().first()


async def get_tasks(
    session: AsyncSession,
    project_id: uuid.UUID | None = None,
    manager_id: uuid.UUID | None = None,
    is_completed: bool | None = None,
    search: str | None = None,
    deadline_to: datetime | None = None,
) -> list[Task] | None:
    stmt = select(Task)

    if project_id:
        stmt = stmt.where(Task.project_id == project_id)
    if manager_id:
        stmt = stmt.where(Task.manager_id == manager_id)
    if is_completed is not None:
        stmt = stmt.where(Task.completed == is_completed)
    if deadline_to:
        stmt = stmt.where(Task.due_date >= deadline_to)
    if search:
        stmt = stmt.where(Task.title.ilike(f"%{search}%"))

    result = await session.execute(stmt.order_by(Task.created_at.desc()))
    return result.scalars().all()


async def delete_task(session: AsyncSession, task_id: uuid.UUID) -> None:
    task = await get_task(session, task_id)
    if not task:
        return None
    await session.delete(task)
    await session.commit()
    return task
