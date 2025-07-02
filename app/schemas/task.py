import uuid
from datetime import datetime
from pydantic import BaseModel

class TaskUserRead(BaseModel):
    title: str
    description: str | None = None
    
class TaskBase(TaskUserRead):
    due_date: datetime | None = None
    project_id: uuid.UUID
    manager_id: uuid.UUID

    model_config = {"from_attributes": True}


class TaskCreate(TaskBase):
    pass


class TaskRead(TaskBase):
    id: uuid.UUID
    completed: bool
    created_at: datetime

