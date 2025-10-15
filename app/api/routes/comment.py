import uuid
from fastapi import Request
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.auth import get_current_active_auth_user
from app.models.user import User
from app.core.config import ALL
from app.core.database import get_db
from app.crud.auth import require_role
from app.crud.comment import create_comment, get_all_comments, delete_comment, get_comment, update_comment
from app.schemas.comment import CommentCreate, CommentRead
from app.utils.exceptions import get_or_404, handle_db_exceptions

router = APIRouter(prefix="/comments", tags=["Comments"])


@router.get("/", response_model=list[CommentRead])
async def read_all(
    session: AsyncSession = Depends(get_db),
    user=Depends(require_role(ALL)),
):
    comments = await get_all_comments(session)
    return comments

# @handle_db_exceptions
@router.post("/", response_model=CommentRead)
async def create(
    comment_in: CommentCreate,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_auth_user),
):
  
    return await create_comment(session, comment_in, current_user)


@router.get("/{comment_id}", response_model=CommentRead)
async def read(
    comment_id: uuid.UUID,
    session: AsyncSession = Depends(get_db),
    user=Depends(require_role(ALL)),
):
    comment = get_or_404(await get_comment(session, comment_id), "Comment not found")
    return comment

@router.put("/{comment_id}", response_model=CommentRead)
async def update_comment_by_id(
    comment_id: uuid.UUID,
    comment_in: CommentCreate,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_auth_user),
):
    comment = get_or_404(await get_comment(session, comment_id), "Comment not found")
    if comment.author_id != current_user.id:
        return {"error": "You do not have permission to update this comment."}
    updated_comment = await update_comment(session, comment_id, comment_in)
    return updated_comment
   

@router.delete("/{comment_id}", status_code=200)
async def delete_comment_by_id(
    comment_id: uuid.UUID,
    session: AsyncSession = Depends(get_db),
    user=Depends(require_role(ALL)),
):
    get_or_404(await delete_comment(session, comment_id), "Comment not found")
    return {"message": "Comment deleted"}
