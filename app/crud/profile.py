import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.profile import Profile
from app.schemas.profile import ProfileCreate, ProfileUpdate


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


async def update_profile(
    session: AsyncSession, user_id: uuid.UUID, profile_in: ProfileUpdate
) -> Profile | None:
    profile = await get_profile_by_id(session, user_id)
    if not profile:
        return None
    if profile_in.avatar_url is not None:
        profile.avatar_url = profile_in.avatar_url
    if profile_in.bio is not None:
        profile.bio = profile_in.bio

    await session.commit()
    await session.refresh(profile)
    return profile


async def delete_profile_by_id(session: AsyncSession, user_id: uuid.UUID) -> None:
    profile = await get_profile_by_id(session, user_id)
    if not profile:
        return None
    await session.delete(profile)
    await session.commit()
    return profile
