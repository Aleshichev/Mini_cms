from pydantic import BaseModel, HttpUrl
import uuid


class ProfileBase(BaseModel):
    avatar_url: HttpUrl | None = None
    bio: str | None = None
    user_id: uuid.UUID


class ProfileCreate(ProfileBase):
    pass


class ProfileRead(ProfileBase):
    id: uuid.UUID
