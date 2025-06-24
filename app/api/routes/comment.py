from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
import uuid

from app.schemas.comment import CommentCreate, CommentRead
from app.crud.comment import create_comment, get_comment
from app.core.database import get_db

router = APIRouter(prefix="/comments", tags=["Comments"])

@router.post("/", response_model=CommentRead)
async def create(comment_in: CommentCreate, session: AsyncSession = Depends(get_db)):
    return await create_comment(session, comment_in)

@router.get("/{comment_id}", response_model=CommentRead)
async def read(comment_id: uuid.UUID, session: AsyncSession = Depends(get_db)):
    comment = await get_comment(session, comment_id)
    if not comment:
        raise HTTPException(404, detail="Comment not found")
    return comment
