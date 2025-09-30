import logging
import subprocess
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware

from fastapi import FastAPI

from app.api.roter import api_router
from app.core.config import settings
from app.core.database import async_session, dispose
from app.db.init_db import init_db
from app.taskiq_broker import broker
# from app.utils.retry_broker import startup_with_retry
from app.middleware import register_middlewares


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
    # await startup_with_retry(broker)   # taskiq
    yield
    # shutdown
    logger.info("dispose engine")
    dispose()
    # await broker.shutdown()            # taskiq


main_app = FastAPI(lifespan=lifespan, title=settings.PROJECT_NAME)

main_app.include_router(api_router)

main_app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


register_middlewares(main_app)