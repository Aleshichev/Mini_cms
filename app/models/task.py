import uuid
from datetime import datetime
from sqlalchemy import String, Text, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    due_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    completed: Mapped[bool] = mapped_column(Boolean, default=False)
    
    manager_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    deal_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("deals.id"))

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow
    )
    
    manager: Mapped["User"] = relationship(back_populates="tasks")
    deal: Mapped["Deal"] = relationship(back_populates="tasks")
