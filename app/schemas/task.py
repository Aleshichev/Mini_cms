from __future__ import annotations   
import uuid
from datetime import datetime
from typing import List
from pydantic import BaseModel


class TaskRead(BaseModel):
    id: uuid.UUID
    title: str
    description: str | None = None
    due_date: datetime | None = None
    completed: bool

    model_config = {"from_attributes": True}


class TaskCreate(BaseModel):
    title: str
    description: str | None = None
    due_date: datetime | None = None
    completed: bool = False
    project_id: uuid.UUID
    manager_id: uuid.UUID



class TaskUpdate(TaskCreate):
    pass


class TaskDetailRead(TaskRead):
    pass
    # project: ProjectBase | None = None
    comments: List[CommentBase] = []
    manager: UserBase | None = None

from app.schemas.comment import CommentBase
from app.schemas.user import UserBase
# from app.schemas.project import ProjectBase


TaskDetailRead.model_rebuild()


