from pydantic import BaseModel, field_validator
import uuid


class ProfileBase(BaseModel):
    avatar_url: str | None = None
    bio: str | None = None
    user_id: uuid.UUID
    
    @field_validator("avatar_url")
    def validate_avatar_url(cls, v: str):
        if v is not None and not v.startswith("https://"):
            raise ValueError("The avatar url must start with https://")
        return v


class ProfileCreate(ProfileBase):
    pass


class ProfileRead(ProfileBase):
    id: uuid.UUID
