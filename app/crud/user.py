from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.utils.security import hash_password
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
import uuid


async def get_all_users(session: AsyncSession) -> list[User]:
    result = await session.execute(select(User))
    return result.scalars().all()


async def get_user_by_email(session: AsyncSession, email: str) -> User | None:
    stmt = (
        select(User)
        .where(User.email == email)
        .options(
            selectinload(User.profile),
            selectinload(User.deals),
            selectinload(User.tasks),
            selectinload(User.comments),
            selectinload(User.projects),
        )
    )
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


async def get_user_by_telegram_id(
    session: AsyncSession, telegram_id: int
) -> User | None:
    stmt = select(User).where(User.telegram_id == telegram_id)
    result = await session.execute(stmt)
    return result.scalars().first()

async def get_user_by_id(
    session: AsyncSession, user_id: uuid.UUID
) -> User | None: 
    return await session.get(User, user_id)


async def update_user(
    session: AsyncSession, user_id: uuid.UUID, user_in: UserUpdate
) -> User | None:
    user = await session.get(User, user_id)
    if not user:
        return None

    user_data = user_in.model_dump(exclude_unset=True)

    for field, value in user_data.items():
        if field == "hashed_password":
            value = hash_password(value)
        setattr(user, field, value)

    await session.commit()
    await session.refresh(user)
    return user


async def delete_user(session: AsyncSession, user_id: uuid.UUID) -> None:
    user = await session.get(User, user_id)
    if not user:
        return None

    await session.delete(user)
    await session.commit()
    return user
