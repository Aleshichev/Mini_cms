# from app.celery_app import celery_app
# from app.crud.task import get_task  # твой crud
# from app.core.database import get_db_context  # твоя сессия
# import asyncio


# @celery_app.task
# def notify_about_task(task_id: str):
#     asyncio.run(_notify_async(task_id))


# async def _notify_async(task_id: str):
#     # async for session in get_db():
#     async with get_db_context() as session:
#         task = await get_task(session, task_id)
#         print(f"🔔 Уведомление: создана задача для {task.manager_id}")
