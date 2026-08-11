from sqlalchemy import String, Boolean, DateTime, Enum, Text, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid import UUID
import enum
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from backend.src.db.database import Base

class ReportStatus(enum.Enum):
    DRAFT = "draft"
    PENDING_APPROVAL = "pending_approval"
    APPROVED = "approved"
    REJECTED = "rejected"
    PUBLISHED = "published"
    SENT = "sent"

class ReportFormat(enum.Enum):
    PDF = "pdf"
    HTML = "html"
    CSV = "csv"

class ReportTemplate(Base):
    __tablename__ = "report_templates"

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    template_content: Mapped[str] = mapped_column(Text, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)

class Report(Base):
    __tablename__ = "reports"

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, unique=True, nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    template_id: Mapped[UUID | None] = mapped_column(PG_UUID(as_uuid=True), nullable=True)
    country_filter: Mapped[str | None] = mapped_column(String(64), nullable=True)
    language_filter: Mapped[str | None] = mapped_column(String(64), nullable=True)
    date_from: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    date_to: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    min_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    status: Mapped[ReportStatus] = mapped_column(Enum(ReportStatus), nullable=False, default=ReportStatus.DRAFT)
    content_html: Mapped[str | None] = mapped_column(Text, nullable=True)
    approved_by: Mapped[UUID | None] = mapped_column(PG_UUID(as_uuid=True), nullable=True)
    approved_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    published_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    created_by: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    template = relationship("ReportTemplate")
