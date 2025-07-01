from uuid import uuid4, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text, DateTime, Enum
from datetime import datetime
from app.models import Base
import enum


class ProjectsName(enum.Enum):
    web_site = "web_site"
    mobile_app = "mobile_app"
    desktop_app = "desktop_app"
    telegram_bot = "telegram_bot"


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    name: Mapped[ProjectsName] = mapped_column(Enum(ProjectsName), nullable=False, default=ProjectsName.web_site)
    description: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow
    )
    deals: Mapped[list["Deal"]] = relationship(
        back_populates="project", cascade="all, delete-orphan"
    )

    users: Mapped[list["User"]] = relationship(
        "User", secondary="users_projects", back_populates="projects", passive_deletes=True
    )
    tasks: Mapped[list["Task"]] = relationship(back_populates="project")
