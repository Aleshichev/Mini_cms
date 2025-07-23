import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.comment import Comment
from app.schemas.comment import CommentCreate


async def create_comment(session: AsyncSession, comment_in: CommentCreate) -> Comment:
    comment = Comment(**comment_in.model_dump())
    session.add(comment)
    await session.commit()
    await session.refresh(comment)
    return comment


async def get_comment(session: AsyncSession, comment_id: uuid.UUID) -> Comment | None:
    result = await session.execute(select(Comment).where(Comment.id == comment_id))
    return result.scalars().first()


async def delete_comment(session: AsyncSession, comment_id: uuid.UUID) -> None:
    comment = await get_comment(session, comment_id)
    if not comment:
        return None
    await session.delete(comment)
    await session.commit()
    return comment
