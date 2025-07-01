import uuid
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, field_validator
from app.models.user import UserRole


class UserBase(BaseModel):
    full_name: str = Field(..., min_length=1, max_length=255)
    email: EmailStr
    role: UserRole = UserRole.manager
    is_active: bool = True
    telegram_id: int | None = None


class UserCreate(UserBase):
    hashed_password: str = Field(..., min_length=6, max_length=100)

    @field_validator("hashed_password")
    def validate_password(cls, v):
        if len(v) < 6:
            raise ValueError("The password is too short")
        if not any(char.isdigit() for char in v):
            raise ValueError("The pasword must contain at least one number")
        if not any(char.isupper() for char in v):
            raise ValueError("The password must contain at least one uppercase letter")
        return v


class UserRead(UserBase):
    id: uuid.UUID
    created_at: datetime

    class Config:
        from_attributes = True
