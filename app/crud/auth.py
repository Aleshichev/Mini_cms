from sqlalchemy.ext.asyncio import AsyncSession
from app.utils.security import verify_password
from fastapi import Depends, Form, HTTPException, status
from app.crud.user import get_user_by_email
from app.core.database import get_db  
from app.schemas.user import UserJWT
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.utils.jwt import decode_jwt
from jwt.exceptions import InvalidTokenError
from app.utils.jwt import TOKEN_TYPE_FIELD
from app.redis import redis_client
from app.utils.jwt import EXPIRE_MINUTES

http_bearer = HTTPBearer()
BLACKLIST_TTL = EXPIRE_MINUTES * 60


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


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
):
    token = credentials.credentials
    try:
        payload = await decode_jwt(token)
        # payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_email: str = payload.get("sub")
        role: str = payload.get("role")
        if user_email is None or role is None:
            raise HTTPException(
                status_code=401,
                detail="Could not validate credentials",
            )
        return {"email": user_email, "role": role}
    except InvalidTokenError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")


def require_role(required_roles: list[str]):
    def role_checker(current_user: dict = Depends(get_current_user)):
        if current_user["role"] not in required_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied: insufficient permissions",
            )
        return current_user

    return role_checker


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
    jti = payload.get("jti")
    blacklist_key = f"blacklist:{jti}"
    if await redis_client.get(blacklist_key):
        raise HTTPException(status_code=401, detail="Token is blacklisted")
    return payload


async def get_current_auth_user(
    payload: dict = Depends(get_current_token_payload),
    session: AsyncSession = Depends(get_db),
) -> UserJWT:
    token_type = payload.get(TOKEN_TYPE_FIELD)
    if token_type != "access":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token type",
        )
    email: str = payload.get("sub")
    if user := await get_user_by_email(session, email):
        return user
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="User not found",
    )


async def get_auth_user_for_refresh(
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
    payload: dict = Depends(get_current_token_payload),
    session: AsyncSession = Depends(get_db),
) -> UserJWT:
    token = credentials.credentials
    token_type = payload.get(TOKEN_TYPE_FIELD)
    if token_type != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token type",
        )
    email: str = payload.get("sub")
    # jti: str = payload.get("jti")

    key = f"refresh:{email}"
    stored = await redis_client.get(key)
    if stored is None or stored != token:
        # либо истек, либо уже отозван
        raise HTTPException(401, "Invalid refresh token")

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


async def logout_by_token(token: str):
    try:
        payload = await decode_jwt(token)
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )
    email = payload.get("sub")
    jti: str = payload.get("jti")

    key_refresh = f"refresh:{email}"
    key_access = f"access:{email}:{jti}"

    deleted = await redis_client.delete(key_refresh)
    if deleted == 0:
        raise HTTPException(
            status_code=401, detail="Token already expired or logged out"
        )
    await redis_client.delete(key_access)
    blacklist_key = f"blacklist:{jti}"
    await redis_client.set(blacklist_key, "true", ex=int(BLACKLIST_TTL))

    return {"message": "Successfully logged out"}
