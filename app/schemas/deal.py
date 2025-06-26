import uuid
from datetime import datetime
from pydantic import BaseModel
from app.schemas.client import ClientBase
from app.schemas.user import UserBase
from app.models.deal import DealStatus


class DealBase(BaseModel):
    title: str
    description: str | None = None
    status: str = DealStatus.new 
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
