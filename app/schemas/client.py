import uuid
import re
from datetime import datetime
from pydantic import BaseModel, EmailStr, field_validator


class ClientBase(BaseModel):
    full_name: str
    phone: str | None = None
    email: EmailStr | None = None
    
    @field_validator("phone")
    def validate_phone(cls, v: str):
        if v is None:
            return v
        if not re.fullmatch(r"\+\d{11}", v):
            raise ValueError("Телефон должен начинаться с + и содержать 11 цифр")
        return v
    

class ClientCreate(ClientBase):
    pass


class ClientRead(ClientBase):
    id: uuid.UUID
    created_at: datetime
    
    class Config:
        from_attributes = True