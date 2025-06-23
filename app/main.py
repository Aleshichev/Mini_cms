from fastapi import FastAPI
from app.core.config import settings
from contextlib import asynccontextmanager
from app.core.database import dispose
from app.api.roter import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    yield
    # shutdown
    print("dispose engine")
    dispose()


main_app = FastAPI(lifespan=lifespan, title=settings.PROJECT_NAME)

main_app.include_router(api_router)
