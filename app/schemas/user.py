from __future__ import annotations

import uuid
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field, field_validator

from app.models.user import UserRole


class UserJWT(BaseModel):
    # username: str
    email: EmailStr | None = None
    full_name: str
    role: UserRole
    active: bool = True


class UserBase(BaseModel):
    full_name: str = Field(..., min_length=1, max_length=255)
    email: EmailStr
    role: UserRole = UserRole.manager
    is_active: bool = True
    telegram_id: int | None = None

    model_config = {"from_attributes": True}


class UserCreate(UserBase):
    password: str = Field(..., min_length=6, max_length=100)

    @field_validator("password")
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


class UserUpdate(UserBase):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None
    telegram_id: Optional[int] = None
    hashed_password: Optional[str] = None


class UserDetail(UserRead):
    tasks: List["TaskUserRead"] = []
    deals: List["DealRead"] = []
    projects: List["ProjectBase"] = []


from app.schemas.deal import DealRead
from app.schemas.project import ProjectBase
from app.schemas.task import TaskUserRead

UserDetail.model_rebuild()
