import uuid
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import ALL
from app.core.database import get_db
from app.crud.auth import require_role
from app.crud.task import (
    create_task,
    delete_task,
    get_task,
    get_tasks,
    update_task,
)
from app.schemas.task import TaskCreate, TaskRead, TaskUpdate, TaskDetailRead
from app.utils.exceptions import get_or_404

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post("/", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
async def create_new_task(
    task_in: TaskCreate,
    session: AsyncSession = Depends(get_db),
    user=Depends(require_role(ALL)),
):
    new_task = await create_task(session, task_in)
    return new_task


@router.get("/", response_model=list[TaskRead])
async def read_tasks(
    session: AsyncSession = Depends(get_db),
    user=Depends(require_role(ALL)),
):
    tasks = await get_tasks(session)
    get_or_404(tasks, "Tasks not found")
    return tasks


@router.get("/{task_id}", response_model=TaskDetailRead)
async def read_task(
    task_id: uuid.UUID,
    session: AsyncSession = Depends(get_db),
    user=Depends(require_role(ALL)),
):
    task = get_or_404(await get_task(session, task_id), "Task not found")
    return task


@router.put("/{task_id}", response_model=TaskRead)
async def update_task_by_id(
    task_id: uuid.UUID,
    task_in: TaskUpdate,
    session: AsyncSession = Depends(get_db),
    user=Depends(require_role(ALL)),
):
    task = get_or_404(await update_task(session, task_id, task_in), "Task not found")
    return task


@router.delete("/{task_id}", status_code=200)
async def delete_task_by_id(
    task_id: uuid.UUID,
    session: AsyncSession = Depends(get_db),
    user=Depends(require_role(ALL)),
):
    get_or_404(await delete_task(session, task_id), "Task not found")
    return {"message": "Task deleted"}
