import uuid

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession
import shutil
from pathlib import Path
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

UPLOAD_DIR = Path("media/avatars")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


def save_uploaded_file(file: UploadFile) -> str:
    ext = Path(file.filename).suffix
    filename = f"{uuid.uuid4()}{ext}"
    filepath = UPLOAD_DIR / filename

    with filepath.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return f"/media/avatars/{filename}"


@router.post("/", response_model=ProfileRead)
async def create_new_profile(
    user_id: uuid.UUID = Form(...),
    bio: str = Form(""),
    avatar_url: UploadFile = File(None),
    session: AsyncSession = Depends(get_db),
    user=Depends(require_role(ALL)),
):

    avatar_path = save_uploaded_file(avatar_url) if avatar_url else None
    profile_in = ProfileCreate(
        user_id=user_id,
        avatar_url=avatar_path,
        bio=bio,
    )

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
    bio: str = Form(""),
    avatar_url: UploadFile = File(None),
    session: AsyncSession = Depends(get_db),
    user=Depends(require_role(ALL)),
):

    avatar_path = (
        save_uploaded_file(avatar_url) if avatar_url else None
    )
    profile_in = ProfileUpdate(
        user_id=user_id,
        avatar_url=avatar_path,
        bio=bio,
    )

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
