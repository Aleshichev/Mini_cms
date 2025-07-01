from fastapi import FastAPI
from app.core.config import settings
from contextlib import asynccontextmanager
from app.core.database import dispose
from app.api.roter import api_router
import logging
from app.core.database import async_session
from app.db.init_db import init_db
import subprocess


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("--------------------🚀 Starting application...")
    logger.info(f"--------------------📦 DATABASE_URL: {settings.DATABASE_URL}")
    try:
        subprocess.run(["alembic", "upgrade", "head"], check=True)
        logger.info("---------------✅ Migrations applied")
    except subprocess.CalledProcessError as e:
        logger.error("-----------------❌ Migration failed")
        raise e

    async with async_session() as session:
        await init_db(session)
    yield
    # shutdown
    logger.info("dispose engine")
    dispose()


main_app = FastAPI(lifespan=lifespan, title=settings.PROJECT_NAME)

main_app.include_router(api_router)
