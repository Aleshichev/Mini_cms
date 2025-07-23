import sys
import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.pool import NullPool
from app.core.config import Settings
from app.core.database import get_db
from app.main import main_app as app
import os
from httpx import AsyncClient, ASGITransport
from app.crud.user import create_user
from app.schemas.user import UserCreate
from app.utils.security import hash_password

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Укажи тестовую env
os.environ["ENV_FILE"] = ".env.test"

settings = Settings()

# Создаём тестовый engine
test_engine = create_async_engine(
    settings.DATABASE_URL, poolclass=NullPool, future=True
)
TestSessionLocal = async_sessionmaker(test_engine, expire_on_commit=False)


# Переопределяем get_db


async def override_get_db():
    async with TestSessionLocal() as session:
        yield session


# Подключаем зависимость
app.dependency_overrides[get_db] = override_get_db


# Фикстура клиента
@pytest_asyncio.fixture
async def async_client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client


# @pytest_asyncio.fixture
# async def db_session():
#     db_generator = override_get_db()
#     db = await db_generator.__anext__()
#     yield db
#     await db_generator.aclose()

# @pytest_asyncio.fixture
# async def get_auth_header(async_client, db_session):
#     await create_user(
#         db_session,
#         UserCreate(
#             email="admin@example.com",
#             hashed_password="admin1Aassword",
#             full_name="Admin",
#             telegram_id=12345678,
#             role="admin",
#         ),
#     )

#     login = await async_client.post(
#         "/auth/login/",
#         data={"username": "admin@example.com", "password": "adminpassword"},
#     )

#     token = login.json()["access_token"]
#     return {"Authorization": f"Bearer {token}"}
