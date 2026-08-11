from sqlalchemy import String, Boolean, DateTime, Enum
from sqlalchemy.orm import Mapped, mapped_column
from uuid import UUID
import enum
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from backend.src.db.database import Base

class UserRole(enum.Enum):
    ADMIN = "admin"
    MANAGER = "manager"
    NEWS_OPERATOR = "news_operator"
    VIEWER = "viewer"

class User(Base):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(320), unique=True, nullable=False, index=True)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(256), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    last_login: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
