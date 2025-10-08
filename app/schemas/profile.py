import uuid
from typing import Optional

from pydantic import BaseModel, field_validator


class ProfileBase(BaseModel):
    user_id: uuid.UUID
    avatar_url: str | None = None
    bio: str | None = None

    # @field_validator("avatar_url")
    # def validate_avatar_url(cls, v: str):
    #     if v is not None and not v.startswith("https://"):
    #         raise ValueError("The avatar url must start with https://")
    #     return v


class ProfileCreate(ProfileBase):
    pass


class ProfileUpdate(ProfileBase):
    avatar_url: Optional[str] = None
    bio: Optional[str] = None


class ProfileRead(ProfileCreate):
    pass
 