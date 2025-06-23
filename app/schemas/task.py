import uuid
from datetime import datetime
from pydantic import BaseModel

class TaskBase(BaseModel):
    title: str
    description: str | None = None
    due_date: datetime | None = None

class TaskCreate(TaskBase):
    deal_id: uuid.UUID
    manager_id: uuid.UUID

class TaskRead(TaskBase):
    id: uuid.UUID
    completed: bool
    created_at: datetime
    deal_id: uuid.UUID
    manager_id: uuid.UUID

    class Config:
        orm_mode = True
