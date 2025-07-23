import logging
import random
import uuid

from faker import Faker
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.data import PROJECTS, USERS
from app.models import Comment, Deal, Profile, Project, Task, User
from app.models.client import Client
from app.models.project import ProjectsName
from app.models.user import UserRole
from app.utils.security import hash_password

logger = logging.getLogger(__name__)
fake = Faker("en_US")


async def init_db(session: AsyncSession):
    logger.info("----------------Initializing database...")

    result = await session.execute(select(User))
    if result.scalars().first():
        logger.info("-------------User data already exists in the database.")
        return
    for i, user_data in enumerate(USERS):

        user = User(
            id=uuid.uuid4(),
            full_name=user_data["full_name"],
            email=user_data["email"],
            hashed_password=hash_password("admin123"),
            role=user_data["role"],
            is_active=True,
            telegram_id=int(1234565) + i,
        )
        session.add(user)
        await session.flush()

        profile = Profile(
            user_id=user.id,
            avatar_url="https://example/200",
            bio=fake.text(max_nb_chars=100),
        )
        session.add(profile)
        await session.flush()

    users_result = await session.execute(select(User))
    all_users = users_result.scalars().all()
    managers = [user for user in all_users if user.role == UserRole.manager]

    # Отдельно получаем менеджеров

    for i, project_data in enumerate(PROJECTS):
        client = Client(
            id=uuid.uuid4(),
            full_name=fake.name(),
            phone="+123456789012",
            email=fake.email(),
            telegram_id=int(12345) + i,
        )
        session.add(client)
        await session.flush()

        users = random.sample(all_users, 2)

        project = Project(
            name=project_data["name"],
            description=project_data["description"],
            users=users,
        )
        session.add(project)
        await session.flush()

        manager = random.choice(managers)
        task = Task(
            title=fake.text(max_nb_chars=50),
            description=fake.text(max_nb_chars=100),
            due_date=fake.date_object(),
            completed=False,
            project_id=project.id,
            manager_id=manager.id,
        )

        session.add(task)
        await session.flush()

        author = random.choice(all_users)
        comment = Comment(
            id=uuid.uuid4(),
            content=fake.text(max_nb_chars=100),
            task_id=task.id,
            author_id=author.id,
        )

        session.add(comment)
        await session.flush()

        deal = Deal(
            id=uuid.uuid4(),
            title=fake.text(max_nb_chars=30),
            description=fake.text(max_nb_chars=100),
            status="new",
            client_id=client.id,
            manager_id=manager.id,
            project_id=project.id,
        )
        session.add(deal)
        await session.flush()

    await session.commit()
    logger.info("---------------------Database initialized. ")
