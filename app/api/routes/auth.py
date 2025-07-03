from app.utils.jwt import encode_jwt, decode_jwt
from app.utils.security import hash_password, verify_password
from app.schemas.user import UserJWT
from fastapi import APIRouter, Depends, Form, HTTPException, status
from pydantic import BaseModel
from app.crud.user import get_user_by_email
from app.core.database import get_db  # или твой путь к сессии
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/auth", tags=["Auth"])


class TokenInfo(BaseModel):
    access_token: str
    token_type: str


async def validate_auth_user(
    email: str = Form(),
    password: str = Form(),
    session: AsyncSession = Depends(get_db),
):
    user = await get_user_by_email(session=session, email=email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email",
        )
    if not verify_password(password, user.hashed_password,):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password",
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Inactive user",
        )
    return user


@router.post("/login/", response_model=TokenInfo)
async def auth_user_issue_jwt(
    user: UserJWT = Depends(validate_auth_user),
):
    jwt_payload = {
        "sub": user.hashed_password,
        "username": user.email,
        "email": user.email,
    }
    token = await encode_jwt(jwt_payload)
    return TokenInfo(
        access_token=token,
        token_type="Bearer",
    )
