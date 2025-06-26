from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.profile import ProfileRead, ProfileCreate
from app.crud.profile import create_profile, get_profile_by_id
from app.core.database import get_db
import uuid

router = APIRouter(prefix="/profiles", tags=["Profile"])


@router.post("/", response_model=ProfileRead)
async def create_new_profile(
    profile_in: ProfileCreate,
    session: AsyncSession = Depends(get_db),
):
    profile = await get_profile_by_id(session, profile_in.user_id)
    if profile:
        raise HTTPException(400, detail="Profile already exists")
    return await create_profile(session, profile_in)


@router.get("/{profile_id}", response_model=ProfileRead)
async def get_profile_details(
    profile_id: uuid.UUID, session: AsyncSession = Depends(get_db)
):
    profile = await get_profile_by_id(session, profile_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile
