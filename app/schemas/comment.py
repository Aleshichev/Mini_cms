import uuid
from datetime import datetime

from pydantic import BaseModel


class CommentBase(BaseModel):
    id: uuid.UUID
    content: str

    model_config = {"from_attributes": True}


class CommentCreate(CommentBase):
    task_id: uuid.UUID
    author_id: uuid.UUID | None = None  # если автор может быть анонимным


class CommentRead(CommentBase):
    created_at: datetime
    task_id: uuid.UUID
    author_id: uuid.UUID | None


class CommentUserRead(CommentBase):
    created_at: datetime
