import enum
import uuid

from sqlalchemy.dialects.postgresql import UUID
from app.models.base import Base
from datetime import datetime
from sqlalchemy import String, Boolean, DateTime, BigInteger, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

class UserRole(enum.Enum):
    admin = "admin"
    manager = "manager"


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    full_name: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=False, unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole), default=UserRole.manager, nullable=False
    )
    telegram_id: Mapped[int | None] = mapped_column(
        BigInteger, unique=True, nullable=True
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow
    )

    deals: Mapped[list["Deal"]] = relationship(
        back_populates="manager", cascade="all, delete-orphan"
    )
