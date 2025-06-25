# app/api/routes/project.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.project import ProjectCreate, ProjectRead
from app.crud.project import create_project, get_project_by_id
from app.core.database import get_db
import uuid


router = APIRouter(prefix="/projects", tags=["Projects"])


@router.post("/", response_model=ProjectRead)
async def create_new_project(
    data: ProjectCreate, session: AsyncSession = Depends(get_db)
):
    return await create_project(session, data)


@router.get("/{project_id}", response_model=ProjectRead)
async def read_project(project_id: uuid.UUID, session: AsyncSession = Depends(get_db)):
    project = await get_project_by_id(session, project_id)
    if not project:
        raise HTTPException(404, detail="Проект не найден")
    return project
