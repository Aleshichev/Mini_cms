# app/api/routes/project.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.project import ProjectCreate, ProjectRead, ProjectUpdate
from app.crud.project import (
    create_project,
    get_project_by_id,
    update_users_by_project,
    delete_project,
)
from app.core.database import get_db
from app.utils.exceptions import get_or_404
import uuid
from app.core.config import AM, ALL
from app.crud.auth import require_role


router = APIRouter(prefix="/projects", tags=["Projects"])


@router.post("/", response_model=ProjectRead)
async def create_new_project(
    data: ProjectCreate,
    session: AsyncSession = Depends(get_db),
    user=Depends(require_role(AM)),
):
    return await create_project(session, data)


@router.get("/{project_id}", response_model=ProjectRead)
async def read_project(
    project_id: uuid.UUID,
    session: AsyncSession = Depends(get_db),
    user=Depends(require_role(AM)),
):
    project = await get_project_by_id(session, project_id)
    if not project:
        raise HTTPException(404, detail="Project not found")
    return project


@router.patch("/{project_id}", response_model=ProjectRead)
async def add_users_project(
    project_id: uuid.UUID,
    data: ProjectUpdate,
    session: AsyncSession = Depends(get_db),
    user=Depends(require_role(ALL)),
):
    project = await update_users_by_project(session, project_id, data)
    if not project:
        raise HTTPException(404, detail="Project not found")
    return project


@router.delete("/{project_id}", status_code=200)
async def delete_project_by_id(
    project_id: uuid.UUID,
    session: AsyncSession = Depends(get_db),
    user=Depends(require_role(AM)),
):
    get_or_404(await delete_project(session, project_id), "Project not found")
    return {"message": "Project deleted"}
