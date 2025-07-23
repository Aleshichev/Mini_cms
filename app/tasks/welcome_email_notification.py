import logging
import uuid
from asyncio import sleep

from app.mailling.send_welcome_email import send_welcome_email as send
from app.taskiq_broker import broker

log = logging.getLogger(__name__)


@broker.task
async def send_welcome_email(user_id: uuid.UUID) -> None:
    await sleep(5)
    log.info("Send welcome email to user %s", user_id)
    await send(user_id=user_id)
