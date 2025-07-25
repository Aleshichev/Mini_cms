from contextlib import asynccontextmanager
import pytest
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

engine: AsyncEngine = create_async_engine(
    settings.DATABASE_URL, echo=False, future=True
)

async_session = async_sessionmaker(
    engine, expire_on_commit=False, autoflush=False, autocommit=False
)


async def dispose():
    await engine.dispose()


async def get_db():
    async with async_session() as session:
        yield session


@asynccontextmanager
async def get_db_context():
    async with async_session() as session:
        yield session

@pytest.fixture()
async def db_session():
    async with engine.connect() as conn:
        trans = await conn.begin()
        async_session_for_test = async_sessionmaker(bind=conn, expire_on_commit=False, autoflush=False)

        async with async_session_for_test() as session:
            yield session

        await trans.rollback()