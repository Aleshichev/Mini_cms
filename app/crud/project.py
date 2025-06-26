# app/crud/project.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.project import Project
from app.models.user import User
from app.schemas.project import ProjectCreate
from uuid import UUID
from sqlalchemy.orm import selectinload


async def get_users_by_ids(session: AsyncSession, user_ids: list[UUID]) -> list[User]:
    users = await session.execute(select(User).where(User.id.in_(user_ids)))
    return users.scalars().all()


async def create_project(session: AsyncSession, data: ProjectCreate) -> Project:
    project = Project(
        name=data.name,
        description=data.description,
    )

    if data.users:
        project.users = await get_users_by_ids(session, data.users)
        # users = await session.execute(select(User).where(User.id.in_(data.users)))
        # project.users = users.scalars().all()

    session.add(project)
    await session.commit()
    stmt = select(Project).options(selectinload(Project.users)).where(Project.id == project.id)
    result = await session.execute(stmt)
    return result.scalars().first()


async def get_project_by_id(session: AsyncSession, project_id: UUID) -> Project | None:
    stmt = (
        select(Project)
        .options(selectinload(Project.users))  
        .where(Project.id == project_id)
    )
    result = await session.execute(stmt)
    return result.scalars().first()


async def update_users_by_project(session: AsyncSession, project_id: UUID, data: Project) -> Project | None:
    project = await get_project_by_id(session, project_id)
    if data.name is not None:
        project.name = data.name
    if data.description is not None:
        project.description = data.description
    if data.users is not None:
        project.users = await get_users_by_ids(session, data.users)
        # users = await session.execute(select(User).where(User.id.in_(data.users)))
        # project.users = users.scalars().all()
    await session.commit()
    await session.refresh(project)
    return project