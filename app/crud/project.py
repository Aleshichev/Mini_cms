# app/crud/project.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.project import Project
from app.models.user import User
from app.schemas.project import ProjectCreate
import uuid

async def create_project(session: AsyncSession, data: ProjectCreate) -> Project:
    project = Project(
        name=data.name,
        description=data.description,
    )

    if data.user_ids:
        users = await session.execute(
            select(User).where(User.id.in_(data.user_ids))
        )
        project.users = users.scalars().all()

    session.add(project)
    await session.commit()
    await session.refresh(project)
    return project


async def get_project_by_id(session: AsyncSession, project_id: uuid.UUID) -> Project | None:
    result = await session.execute(
        select(Project).where(Project.id == project_id)
    )
    return result.scalars().first()
