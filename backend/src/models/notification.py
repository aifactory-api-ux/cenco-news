from sqlalchemy import String, Boolean, DateTime, Enum, Text
from sqlalchemy.orm import Mapped, mapped_column
from uuid import UUID
import enum
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from backend.src.db.database import Base

class ChannelType(enum.Enum):
    EMAIL = "email"
    SLACK = "slack"
    WEBHOOK = "webhook"

class NotificationRecipient(Base):
    __tablename__ = "notification_recipients"

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str | None] = mapped_column(String(320), nullable=True)
    slack_webhook: Mapped[str | None] = mapped_column(String(1024), nullable=True)
    webhook_url: Mapped[str | None] = mapped_column(String(1024), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)

class ChannelConfig(Base):
    __tablename__ = "channel_configs"

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    channel_type: Mapped[ChannelType] = mapped_column(Enum(ChannelType), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    config_data: Mapped[str] = mapped_column(Text, default='{}', nullable=False)  # JSON string
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
