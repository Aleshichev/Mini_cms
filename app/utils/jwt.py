import uuid
from datetime import datetime, timedelta, timezone

import jwt

from app.core.config import settings
from app.redis import redis_client
from app.schemas.user import UserJWT

TOKEN_TYPE_FIELD = "type"
ACCESS_TOKEN_TYPE = "access"
REFRESH_TOKEN_TYPE = "refresh"

REFRESH_TTL = timedelta(minutes=settings.auth_jwt.refresh_token_expire_days)
EXPIRE_MINUTES = settings.auth_jwt.access_token_expire_minutes


async def encode_jwt(
    payload: dict,
    private_key: str = settings.auth_jwt.private_key_path.read_text(),
    algorithm: str = settings.auth_jwt.algorithm,
    expire_minutes: int = EXPIRE_MINUTES,
    expire_timadelta: timedelta | None = None,
):
    to_encode = payload.copy()
    now = datetime.now(timezone.utc)
    if expire_timadelta:
        expire = now + expire_timadelta
    else:
        expire = now + timedelta(minutes=expire_minutes)
    to_encode.update(exp=expire, iat=now, jti=str(uuid.uuid4()))
    encoded = jwt.encode(to_encode, private_key, algorithm=algorithm)
    return encoded


async def decode_jwt(
    token: str | bytes,
    public_key: str = settings.auth_jwt.public_key_path.read_text(),
    algorithm: str = settings.auth_jwt.algorithm,
):
    return jwt.decode(token, public_key, algorithms=[algorithm])


async def create_jwt(
    token_type: str,
    token_data: dict,
    expire_minutes: int = EXPIRE_MINUTES,
    expire_timadelta: timedelta | None = None,
) -> str:
    jwt_payload = {TOKEN_TYPE_FIELD: token_type}
    jwt_payload.update(token_data)
    return await encode_jwt(
        payload=jwt_payload,
        expire_timadelta=expire_timadelta,
        expire_minutes=expire_minutes,
    )


async def create_access_token(user: UserJWT):
    jwt_payload = {
        "sub": user.email,
        "name": user.full_name,
        "role": user.role.value,
        # "password": user.hashed_password,
    }
    token = await create_jwt(
        token_type=ACCESS_TOKEN_TYPE,
        token_data=jwt_payload,
        expire_minutes=EXPIRE_MINUTES,
    )
    payload = await decode_jwt(token)
    jti = payload.get("jti")
    key = f"access:{user.email}:{jti}"
    await redis_client.set(key, token, ex=int(EXPIRE_MINUTES * 60))
    return token


async def create_refresh_token(user: UserJWT):
    jwt_payload = {
        "sub": user.email,
    }
    token = await create_jwt(
        token_type=REFRESH_TOKEN_TYPE,
        token_data=jwt_payload,
        expire_timadelta=REFRESH_TTL,
    )
    # payload = await decode_jwt(token)
    # jti = payload.get("jti")
    key = f"refresh:{user.email}"
    await redis_client.set(key, token, ex=int(REFRESH_TTL.total_seconds()))
    return token
