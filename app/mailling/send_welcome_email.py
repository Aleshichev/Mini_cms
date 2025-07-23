import uuid
from asyncio import sleep

from app.core.database import get_db_context
from app.crud.user import get_user_by_id
from app.models.user import User

from .send_email import send_email


async def send_welcome_email(user_id: uuid.UUID) -> None:

    async with get_db_context() as session:
        user = await get_user_by_id(session, user_id)

    await sleep(5)
    await send_email(
        recipient=user.email,
        subject="Registration in the system",
        body=f"Dear, {user.full_name}! You have been registered in the system",
    )
