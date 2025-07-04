from sqlalchemy.ext.asyncio import AsyncSession
from app.utils.security import verify_password
from fastapi import Depends, Form, HTTPException, status
from app.crud.user import get_user_by_email
from app.core.database import get_db  # или твой путь к сессии
from app.schemas.user import UserJWT
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.utils.jwt import decode_jwt
from jwt.exceptions import InvalidTokenError

http_bearer = HTTPBearer()


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
    if not verify_password(
        password,
        user.hashed_password,
    ):
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


async def get_current_token_payload(
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
) -> UserJWT:
    token = credentials.credentials
    try:
        payload = await decode_jwt(token)
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token error",
        )
    return payload


async def get_current_auth_user(
    payload: dict = Depends(get_current_token_payload),
    session: AsyncSession = Depends(get_db),
) -> UserJWT:
    email: str = payload.get("email")
    if user := await get_user_by_email(session, email):
        return user
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="User not found",
    )


async def get_current_active_auth_user(
    user: UserJWT = Depends(get_current_auth_user),
):
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Inactive user",
        )
    return user
