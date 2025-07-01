import uuid
from datetime import datetime
from pydantic import BaseModel

class CommentBase(BaseModel):
    content: str

class CommentCreate(CommentBase):
    task_id: uuid.UUID
    author_id: uuid.UUID | None = None  # если автор может быть анонимным

class CommentRead(CommentBase):
    id: uuid.UUID
    created_at: datetime
    task_id: uuid.UUID
    author_id: uuid.UUID | None

    class Config:
        from_attributes = True
