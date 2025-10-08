import uuid
from datetime import datetime

from sqlalchemy import BigInteger, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Client(Base):
    __tablename__ = "clients"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    phone: Mapped[str | None] = mapped_column(String(13), nullable=True)
    email: Mapped[str | None] = mapped_column(String, nullable=True)
    telegram_id: Mapped[int | None] = mapped_column(
        BigInteger, unique=True, nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow
    )

    deals: Mapped[list["Deal"]] = relationship(
        back_populates="client", cascade="all, delete-orphan", lazy="selectin"
    )
