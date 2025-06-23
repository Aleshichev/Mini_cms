from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
import uuid

from app.schemas.task import TaskCreate, TaskRead
from app.crud.task import create_task, get_task
from app.core.database import get_db

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post("/", response_model=TaskRead)
async def create_new_task(task_in: TaskCreate, session: AsyncSession = Depends(get_db)):
    return await create_task(session, task_in)

@router.get("/{task_id}", response_model=TaskRead)
async def read_task(task_id: uuid.UUID, session: AsyncSession = Depends(get_db)):
    task = await get_task(session, task_id)
    if not task:
        raise HTTPException(404, detail="Task not found")
    return task
