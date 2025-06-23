import uuid
from datetime import datetime
from pydantic import BaseModel, EmailStr
from app.models.user import UserRole


class UserBase(BaseModel):
    full_name: str
    email: EmailStr
    role: UserRole = UserRole.manager
    is_active: bool = True
    telegram_id: int | None = None
    

class UserCreate(UserBase):
    hashed_password: str
    

class UserRead(UserBase):
    id: uuid.UUID
    created_at: datetime