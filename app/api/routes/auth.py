from app.utils.jwt import encode_jwt
from app.schemas.user import UserJWT
from fastapi import APIRouter, Depends
from app.schemas.auth import TokenInfo
from app.crud.auth import validate_auth_user, get_current_active_auth_user

router = APIRouter(prefix="/auth", tags=["Auth"])


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

@router.get("/user/me/")
async def auth_user_check_self_info(
    user: UserJWT = Depends(get_current_active_auth_user),
):
    pass
    return {"username": user.email, "email": user.email}