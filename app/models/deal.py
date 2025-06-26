import uuid
from datetime import datetime
from sqlalchemy import String, ForeignKey, DateTime, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base
import enum

class DealStatus(enum.Enum):
    new = "new"
    in_progress = "in_progress"
    completed = "completed"

class Deal(Base):
    __tablename__ = "deals"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(String(1000), nullable=False)
    description: Mapped[str | None] = mapped_column(String(3000))
    status: Mapped[DealStatus] = mapped_column(Enum(DealStatus), nullable=False, default=DealStatus.new)
    manager_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    client_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("clients.id"))
    project_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("projects.id"))

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow
    )

    manager: Mapped["User"] = relationship(back_populates="deals")
    client: Mapped["Client"] = relationship(back_populates="deals")
    project: Mapped["Project"] = relationship(back_populates="deals")
