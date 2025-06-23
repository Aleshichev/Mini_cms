from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.user import get_user_by_email, create_user
from app.schemas.user import UserCreate, UserRead
from app.core.database import get_db


router = APIRouter(prefix="/user", tags=["Users"])

@router.post("/", response_model=UserRead)
async def create_new_user(user_in: UserCreate, session: AsyncSession = Depends(get_db)):
    user = await get_user_by_email(session, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The user with this email already exists in the system",
        )
    return await create_user(session, user_in)

