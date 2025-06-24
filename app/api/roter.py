from fastapi import APIRouter
from app.api.routes import user, client, deal, task, comment

api_router = APIRouter()
api_router.include_router(user.router)
api_router.include_router(client.router)
api_router.include_router(deal.router)
api_router.include_router(task.router)
api_router.include_router(comment.router)
