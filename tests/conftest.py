import pytest
from httpx import AsyncClient
from app.main import main_app as app  # путь к твоему FastAPI приложению
from app.core.database import get_db  # путь к твоему get_db
from app.core.database import db_session  # фикстура из database.py

@pytest.fixture()
async def async_client(db_session):
    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client

    app.dependency_overrides.clear()
