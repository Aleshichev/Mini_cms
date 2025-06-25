from uuid import uuid4
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text, DateTime
from datetime import datetime
from app.models import Base


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    description: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow
    )
    deals: Mapped[list["Deal"]] = relationship(
        back_populates="project", cascade="all, delete-orphan"
    )

    users: Mapped[list["User"]] = relationship(
        "User", secondary="users_projects", back_populates="projects"
    )
