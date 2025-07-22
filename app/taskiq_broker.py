from taskiq_aio_pika import AioPikaBroker

from app.core.config import settings

broker = AioPikaBroker(
    settings.taskiq.url,
)
