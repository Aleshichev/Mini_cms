from fastapi import APIRouter
from app.api.routes import user, client, deal

api_router = APIRouter()
api_router.include_router(user.router)
api_router.include_router(client.router)
api_router.include_router(deal.router)
