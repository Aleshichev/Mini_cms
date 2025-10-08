from fastapi import APIRouter, Depends
from fastapi.security import HTTPAuthorizationCredentials

from app.crud.auth import (
    get_auth_user_for_refresh,
    get_current_active_auth_user,
    get_current_token_payload,
    http_bearer,
    logout_by_token,
    validate_auth_user,
)
from app.schemas.auth import TokenInfo
from app.schemas.user import UserJWT
from app.utils.jwt import create_access_token, create_refresh_token

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login/", response_model=TokenInfo)
async def auth_user_issue_jwt(
    user: UserJWT = Depends(validate_auth_user),
):
    access_token = await create_access_token(user)
    refresh_token = await create_refresh_token(user)
    return TokenInfo(
        access_token=access_token,
        refresh_token=refresh_token,
    )


@router.post("/logout")
async def logout_user(
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
):
    return await logout_by_token(credentials.credentials)


@router.post("/refresh/", response_model=TokenInfo, response_model_exclude_none=True)
async def auth_refresh_jwt(
    user: UserJWT = Depends(get_auth_user_for_refresh),
):
    access_token = await create_access_token(user)
    return TokenInfo(
        access_token=access_token,
    )


@router.get("/user/me/")
async def auth_user_check_self_info(
    payload: dict = Depends(get_current_token_payload),
    user: UserJWT = Depends(get_current_active_auth_user),
):
    iat = payload.get("iat")

    return {
        "id": user.id,
        "username": user.email,
        "email": user.email,
        "full_name": user.full_name,
        "role": user.role,
        "logged_in_at": iat,
    }
