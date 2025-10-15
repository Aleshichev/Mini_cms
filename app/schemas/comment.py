import uuid
from datetime import datetime

from pydantic import BaseModel


class CommentBase(BaseModel):
    id: uuid.UUID
    content: str

    model_config = {"from_attributes": True}


class CommentCreate(BaseModel):
    task_id: uuid.UUID
    content: str


class CommentRead(CommentBase):
    created_at: datetime
    task_id: uuid.UUID
    author_id: uuid.UUID | None


# class CommentUpdate(BaseModel):
#     content: str
#     task_id: uuid.UUID
#     author_id: uuid.UUID | None


class CommentUserRead(CommentBase):
    created_at: datetime
