import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import ALL, AM
from app.core.database import get_db
from app.crud.auth import require_role
from app.crud.profile import (
    create_profile,
    delete_profile_by_id,
    get_profile_by_id,
    update_profile,
)
from app.schemas.profile import ProfileCreate, ProfileRead, ProfileUpdate
from app.utils.exceptions import get_or_404

router = APIRouter(prefix="/profiles", tags=["Profile"])


@router.post("/", response_model=ProfileRead)
async def create_new_profile(
    profile_in: ProfileCreate,
    session: AsyncSession = Depends(get_db),
    user=Depends(require_role(ALL)),
):
    profile = await get_profile_by_id(session, profile_in.user_id)
    if profile:
        raise HTTPException(400, detail="Profile already exists")
    return await create_profile(session, profile_in)


@router.get("/{user_id}", response_model=ProfileRead)
async def get_profile_details(
    user_id: uuid.UUID,
    session: AsyncSession = Depends(get_db),
    user=Depends(require_role(AM)),
):
    profile = await get_profile_by_id(session, user_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile

@router.put("/{user_id}", response_model=ProfileRead)
@router.patch("/{user_id}", response_model=ProfileRead)
async def update_profile_by_id(
    user_id: uuid.UUID,
    profile_in: ProfileUpdate,
    session: AsyncSession = Depends(get_db),
    user=Depends(require_role(ALL)),
):
    profile = await get_profile_by_id(session, user_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return await update_profile(session, user_id, profile_in)


@router.delete("/{user_id}", status_code=200)
async def delete_profile(
    user_id: uuid.UUID,
    session: AsyncSession = Depends(get_db),
    user=Depends(require_role(ALL)),
):
    get_or_404(await delete_profile_by_id(session, user_id), "Profile not found")
    return {"message": "Profile deleted"}
