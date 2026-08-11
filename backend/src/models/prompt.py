from sqlalchemy import String, Boolean, DateTime, Text
from sqlalchemy.orm import Mapped, mapped_column
from uuid import UUID
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from backend.src.db.database import Base

class Prompt(Base):
    __tablename__ = "prompts"

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    prompt_template: Mapped[str] = mapped_column(Text, nullable=False)
    version: Mapped[str] = mapped_column(String(64), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
