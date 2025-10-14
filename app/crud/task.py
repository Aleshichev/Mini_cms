import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate


async def create_task(session: AsyncSession, task_in: TaskCreate) -> Task:
    task = Task(**task_in.model_dump())
    session.add(task)
    await session.commit()
    await session.refresh(task)
    return task


async def get_task(session: AsyncSession, task_id: uuid.UUID) -> Task | None:
    result = await session.execute(
        select(Task)
        .options(selectinload(Task.comments))
        .options(selectinload(Task.manager))
        .options(selectinload(Task.project))
        .where(Task.id == task_id))
    return result.scalars().first()


async def get_tasks(session: AsyncSession) -> list[Task]:
    result = await session.execute(
        select(Task)
        .options(selectinload(Task.comments))
        .order_by(Task.created_at.desc()))
    return result.scalars().all()


async def update_task(session: AsyncSession, task_id: uuid.UUID, task_in: TaskUpdate) -> Task | None:
    task = await get_task(session, task_id)
    if not task:
        return None

    for field, value in task_in.model_dump(exclude_unset=True).items():
        setattr(task, field, value)

    await session.commit()
    await session.refresh(task)
    return task


async def delete_task(session: AsyncSession, task_id: uuid.UUID) -> Task | None:
    task = await get_task(session, task_id)
    if not task:
        return None
    await session.delete(task)
    await session.commit()
    return task
