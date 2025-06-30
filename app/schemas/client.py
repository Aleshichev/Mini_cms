import uuid
import re
from datetime import datetime
from pydantic import BaseModel, EmailStr, field_validator


class ClientBase(BaseModel):
    full_name: str
    phone: str | None = None
    email: EmailStr | None = None
    telegram_id: int | None = None

    @field_validator("phone")
    def validate_phone(cls, v: str):
        if v is None:
            return v
        
        if len(v) > 13:
            raise ValueError("Phone number must not be longer than 13 characters")
        
        if not re.fullmatch(r"\+\d{12}", v):
            raise ValueError("The phone must start + and contain 12 digits")
        return v


class ClientCreate(ClientBase):
    pass


class ClientRead(ClientBase):
    id: uuid.UUID
    created_at: datetime

    class Config:
        from_attributes = True
