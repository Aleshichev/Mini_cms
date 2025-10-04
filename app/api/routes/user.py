from uuid import UUID

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import ALL, AM, A
from app.core.database import get_db
from app.crud.auth import require_role
from app.crud.user import (
    create_user,
    delete_user,
    get_all_users,
    get_user_by_id,
    get_user_by_email,
    get_user_by_telegram_id,
    update_user,
)
from app.schemas.user import UserCreate, UserDetail, UserRead, UserUpdate
from app.tasks import send_welcome_email
from app.utils.exceptions import get_or_404

router = APIRouter(prefix="/users", tags=["Users"])


@router.get(
    "/",
    response_model=list[UserRead],
)
async def read_users(
    session: AsyncSession = Depends(get_db),
    user=Depends(require_role(A)),
):
    users = await get_all_users(session)
    return users

@router.get("/{user_id}", response_model=UserDetail)
async def read_user_by_id(
    user_id: UUID,
    session: AsyncSession = Depends(get_db),
    user=Depends(require_role(AM)),
):
    user = get_or_404(await get_user_by_id(session, user_id), "User not found")
    return user


@router.get("/by_email/", response_model=UserDetail)
async def read_user_by_email(
    email: str = Query(...),
    session: AsyncSession = Depends(get_db),
    user=Depends(require_role(AM)),
):
    user = get_or_404(await get_user_by_email(session, email), "User not found")
    return user


@router.post("/", response_model=UserRead)
async def create_new_user(
    user_in: UserCreate,
    session: AsyncSession = Depends(get_db),
    user=Depends(require_role(AM)),
    #background_tasks: BackgroundTasks = BackgroundTasks,
):

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
    user = await create_user(session, user_in)
    await send_welcome_email.kiq(user.id)  # taskiq
    # background_tasks.add_task(send_welcome_email, user.id)

    return user

@router.put("/{user_id}", response_model=UserRead)
@router.patch("/{user_id}", response_model=UserRead)
async def update_user_by_id(
    user_id: UUID,
    user_in: UserUpdate,
    session: AsyncSession = Depends(get_db),
    user=Depends(require_role(ALL)),
):
    user = get_or_404(await update_user(session, user_id, user_in), "User not found")
    return user


@router.delete("/{user_id}", status_code=200)
async def delete_user_by_id(
    user_id: UUID,
    session: AsyncSession = Depends(get_db),
    user=Depends(require_role(A)),
):
    get_or_404(await delete_user(session, user_id), "User not found")
    return {"message": "User deleted"}
