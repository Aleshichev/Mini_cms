from fastapi import UploadFile, File, APIRouter
import shutil
import uuid
from pathlib import Path

router = APIRouter()

UPLOAD_DIR = Path("media/avatars")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

@router.post("/upload/avatar/")
async def upload_avatar(file: UploadFile = File(...)):
    file_extension = Path(file.filename).suffix
    file_id = f"{uuid.uuid4()}{file_extension}"
    file_path = UPLOAD_DIR / file_id

    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Возвращаем URL (например, если сервер отдаёт /media статически)
    return {"avatar_url": f"/media/avatars/{file_id}"}
