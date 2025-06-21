import enum
import uuid

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
from app.models.base import Base

class UserRole(enum.Enum):
    admin = "admin"
    manager = "manager"

class User(Base):
    __tablename__ = "users"
    
    id = sa.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    full_name = sa.Column(sa.String, nullable=False)
    email = sa.Column(sa.String, unique=True, nullable=False, index=True)
    hashed_password = sa.Column(sa.String, nullable=False)
    role = sa.Column(sa.Enum(UserRole), nullable=False, default=UserRole.manager)
    telegram_id = sa.Column(sa.BigInteger, unique=True, nullable=True)
    is_active = sa.Column(sa.Boolean, default=True, nullable=False)
    created_at = sa.Column(sa.DateTime(timezone=True), server_default=sa.func.now())

