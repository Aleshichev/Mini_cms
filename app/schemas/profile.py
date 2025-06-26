from pydantic import BaseModel
import uuid


class ProfileBase(BaseModel):
    avatar_url: str | None = None
    bio: str | None = None
    user_id: uuid.UUID


class ProfileCreate(ProfileBase):
    pass


class ProfileRead(ProfileBase):
    id: uuid.UUID
