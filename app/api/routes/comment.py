from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
import uuid
from app.utils.exceptions import handle_db_exceptions

from app.schemas.comment import CommentCreate, CommentRead
from app.crud.comment import create_comment, get_comment, delete_comment
from app.core.database import get_db
from app.utils.exceptions import get_or_404
from app.core.config import ALL
from app.crud.auth import require_role

router = APIRouter(prefix="/comments", tags=["Comments"])


# @handle_db_exceptions
@router.post("/", response_model=CommentRead)
async def create(
    comment_in: CommentCreate,
    session: AsyncSession = Depends(get_db),
    user=Depends(require_role(ALL)),
):
    return await create_comment(session, comment_in)


@router.get("/{comment_id}", response_model=CommentRead)
async def read(
    comment_id: uuid.UUID,
    session: AsyncSession = Depends(get_db),
    user=Depends(require_role(ALL)),
):
    comment = get_or_404(await get_comment(session, comment_id), "Comment not found")
    return comment


@router.delete("/{comment_id}", status_code=200)
async def delete_comment_by_id(
    comment_id: uuid.UUID,
    session: AsyncSession = Depends(get_db),
    user=Depends(require_role(ALL)),
):
    get_or_404(await delete_comment(session, comment_id), "Comment not found")
    return {"message": "Comment deleted"}
