import jwt
from app.core.config import settings
from datetime import datetime, timedelta, timezone


async def encode_jwt(
    payload: dict,
    private_key: str = settings.auth_jwt.private_key_path.read_text(),
    algorithm: str = settings.auth_jwt.algorithm,
    expire_minutes: int = settings.auth_jwt.access_token_expire_minutes,
    expire_timadelta: timedelta | None = None,
):
    to_encode = payload.copy()
    now = datetime.now(timezone.utc)
    if expire_timadelta:
        expire = now + expire_timadelta
    else:
        expire = now + timedelta(minutes=expire_minutes)
    expire = ...
    to_encode.update(exp=expire, iat=now)
    return jwt.encode(payload, private_key, algorithm=algorithm)


async def decode_jwt(
    token: str | bytes,
    public_key: str = settings.auth_jwt.public_key_path.read_text(),
    algorithm: str = settings.auth_jwt.algorithm,
):
    return jwt.decode(token, public_key, algorithms=[algorithm])
