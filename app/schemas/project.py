# app/schemas/project.py
import uuid
from datetime import datetime

from pydantic import BaseModel

from app.models.project import ProjectsName
from app.schemas.user import UserBase
from app.schemas.task import TaskUserRead


class ProjectBase(BaseModel):
    number: int | None = None
    type: ProjectsName = ProjectsName.web_site
    description: str | None = None

    class Config:
        from_attributes = True


class ProjectCreate(ProjectBase):
    users: list[uuid.UUID] = []


class ProjectUpdate(ProjectBase):
    type: str | None = None
    description: str | None = None
    users: list[uuid.UUID] | None = None


class ProjectRead(ProjectCreate):
    id: uuid.UUID
    created_at: datetime
    users: list[UserBase] = []

class ProjectFullRead(ProjectRead):
    tasks: list[TaskUserRead] = []