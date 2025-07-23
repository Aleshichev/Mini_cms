import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import ALL
from app.core.database import get_db
from app.crud.auth import require_role
from app.crud.comment import create_comment, delete_comment, get_comment
from app.schemas.comment import CommentCreate, CommentRead
from app.utils.exceptions import get_or_404, handle_db_exceptions

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
