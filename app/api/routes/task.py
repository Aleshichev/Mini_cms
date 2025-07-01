from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
import uuid
from datetime import datetime
from app.schemas.task import TaskCreate, TaskRead
from app.crud.task import create_task, get_task, get_tasks
from app.core.database import get_db

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post("/", response_model=TaskRead)
async def create_new_task(task_in: TaskCreate, session: AsyncSession = Depends(get_db)):
    return await create_task(session, task_in)


@router.get("/", response_model=list[TaskRead])
async def read_tasks(
    project_id: uuid.UUID | None = None,
    manager_id: uuid.UUID | None = None,
    is_completed: bool | None = None,
    search: str | None = None,
    due_date_to: datetime | None = None,
    session: AsyncSession = Depends(get_db),
):
    tasks = await get_tasks(
        session, project_id, manager_id, is_completed, search, due_date_to
    )
    if not tasks:
        raise HTTPException(404, detail="Tasks not found")
    return tasks


@router.get("/{task_id}", response_model=TaskRead)
async def read_task(task_id: uuid.UUID, session: AsyncSession = Depends(get_db)):
    task = await get_task(session, task_id)
    if not task:
        raise HTTPException(404, detail="Task not found")
    return task
