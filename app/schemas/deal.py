import uuid
from datetime import datetime
from pydantic import BaseModel
from app.models.deal import DealStatus
from app.schemas.client import ClientBase 
from app.schemas.user import UserBase



class DealBase(BaseModel):
    title: str
    description: str | None = None
    status: DealStatus = DealStatus.new
    client_id: uuid.UUID
    manager_id: uuid.UUID
    project_id: uuid.UUID


class DealCreate(DealBase):
    pass


class DealRead(DealBase):
    id: uuid.UUID
    created_at: datetime

    class Config:
        from_attributes = True


class DealReadFull(DealRead):
    client: ClientBase
    manager: UserBase


class DealUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    status: DealStatus | None = None
    client_id: uuid.UUID | None = None
    manager_id: uuid.UUID | None = None
    project_id: uuid.UUID | None = None
