from app.celery_app import celery_app
from app.crud.task import get_task  # твой crud
from app.core.database import get_db  # твоя сессия
import asyncio

@celery_app.task
def notify_about_task(task_id: str):
    asyncio.run(_notify_async(task_id))

async def _notify_async(task_id: str):
    async with get_db() as session:
        task = await get_task(session, task_id)
        print(f"🔔 Уведомление: создана задача для {task.manager_id}")
