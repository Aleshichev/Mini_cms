# app/schemas/project.py
from pydantic import BaseModel, constr
import uuid
from datetime import datetime

class ProjectBase(BaseModel):
    name: str
    description: str | None = None

class ProjectCreate(ProjectBase):
    user_ids: list[uuid.UUID] = []

class ProjectRead(ProjectBase):
    id: uuid.UUID
    created_at: datetime
    user_ids: list[uuid.UUID] = []

    class Config:
        orm_mode = True