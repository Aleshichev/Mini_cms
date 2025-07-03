from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.user import (
    get_user_by_email,
    create_user,
    get_user_by_telegram_id,
    delete_user,
    get_all_users,
    update_user,
)
from app.schemas.user import UserCreate, UserRead, UserDetail, UserUpdate
from app.core.database import get_db
from uuid import UUID
from app.utils.exceptions import get_or_404

router = APIRouter(prefix="/user", tags=["Users"])


@router.get("/", response_model=list[UserRead])
async def read_users(session: AsyncSession = Depends(get_db)):
    users = await get_all_users(session)
    return users


@router.get("/by_email/", response_model=UserDetail)
async def read_user_by_email(
    email: str = Query(...), session: AsyncSession = Depends(get_db)
):
    user = get_or_404(await get_user_by_email(session, email), "User not found")
    return user


@router.post("/", response_model=UserRead)
async def create_new_user(user_in: UserCreate, session: AsyncSession = Depends(get_db)):

    user = await get_user_by_email(session, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The user with this email already exists in the system",
        )

    if user_in.telegram_id is not None:
        existing = await get_user_by_telegram_id(session, user_in.telegram_id)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The user with this telegram id already exists in the system",
            )

    return await create_user(session, user_in)


@router.patch("/{user_id}", response_model=UserRead)
async def update_user_by_id(
    user_id: UUID, user_in: UserUpdate, session: AsyncSession = Depends(get_db)
):
    user = get_or_404(await update_user(session, user_id, user_in), "User not found")
    return user


@router.delete("/{user_id}", status_code=200)
async def delete_user_by_id(user_id: UUID, session: AsyncSession = Depends(get_db)):
    get_or_404(await delete_user(session, user_id), "User not found")
    return {"message": "User deleted"}
