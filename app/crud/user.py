from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.utils.security import hash_password

from app.models.user import User
from app.schemas.user import UserCreate

import uuid


async def get_user_by_email(session: AsyncSession, email: str) -> User | None:
    stmt = select(User).where(User.email == email)
    result = await session.execute(stmt)
    return result.scalars().first()


async def create_user(session: AsyncSession, user_in: UserCreate) -> User:
    hashed = hash_password(user_in.hashed_password)
    user = User(
        id=uuid.uuid4(),
        full_name=user_in.full_name,
        email=user_in.email,
        hashed_password=hashed,
        role=user_in.role,
        is_active=user_in.is_active,
        telegram_id=user_in.telegram_id,
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user

async def get_user_by_telegram_id(session: AsyncSession, telegram_id: int) -> User | None:
    stmt = select(User).where(User.telegram_id == telegram_id)
    result = await session.execute(stmt)
    return result.scalars().first()

