import uuid
from datetime import datetime
from pydantic import BaseModel, EmailStr


class ClientBase(BaseModel):
    full_name: str
    phone: str | None = None
    email: EmailStr | None = None
    

class ClientCreate(ClientBase):
    pass


class ClientRead(ClientBase):
    id: uuid.UUID
    created_at: datetime
    
    class Config:
        from_attributes = True