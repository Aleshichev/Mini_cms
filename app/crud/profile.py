from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.profile import Profile
from app.schemas.profile import ProfileCreate
from app.models.user import User
import uuid


async def get_profile_by_id(
    session: AsyncSession, user_id: uuid.UUID
) -> Profile | None:
    stmt = select(Profile).where(Profile.user_id == user_id)
    result = await session.execute(stmt)
    return result.scalars().first()


async def create_profile(session: AsyncSession, profile_in: ProfileCreate):
    profile = Profile(
        user_id=profile_in.user_id,
        avatar_url=profile_in.avatar_url,
        bio=profile_in.bio,
    )
    session.add(profile)
    await session.commit()
    await session.refresh(profile)
    return profile
