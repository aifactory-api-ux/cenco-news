from sqlalchemy import String, Boolean, DateTime, Enum, Integer, Text, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid import UUID
import enum
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from backend.src.db.database import Base

class NewsSourceType(enum.Enum):
    RSS = "rss"
    WEB_SCRAPE = "web_scrape"
    NEWS_API = "news_api"

class NewsStatus(enum.Enum):
    PENDING = "pending"
    REVIEWED = "reviewed"
    APPROVED = "approved"
    REJECTED = "rejected"
    PUBLISHED = "published"

class Language(enum.Enum):
    SPANISH = "es"
    PORTUGUESE = "pt"
    ENGLISH = "en"

class Country(enum.Enum):
    CHILE = "chile"
    ARGENTINA = "argentina"
    BRAZIL = "brazil"
    PERU = "peru"
    COLOMBIA = "colombia"
    URUGUAY = "uruguay"

class NewsSource(Base):
    __tablename__ = "news_sources"

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    source_type: Mapped[NewsSourceType] = mapped_column(Enum(NewsSourceType), nullable=False)
    url: Mapped[str] = mapped_column(String(1024), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    country: Mapped[Country | None] = mapped_column(Enum(Country), nullable=True)
    language: Mapped[Language | None] = mapped_column(Enum(Language), nullable=True)
    scrape_pattern: Mapped[str | None] = mapped_column(Text, nullable=True)
    polling_interval_minutes: Mapped[int] = mapped_column(Integer, nullable=False, default=60)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    news_items = relationship("NewsItem", back_populates="source")

class NewsItem(Base):
    __tablename__ = "news_items"

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, unique=True, nullable=False)
    title: Mapped[str] = mapped_column(String(1024), nullable=False)
    content_summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    full_content: Mapped[str | None] = mapped_column(Text, nullable=True)
    url: Mapped[str] = mapped_column(String(1024), nullable=False)
    source_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)
    country: Mapped[Country] = mapped_column(Enum(Country), nullable=False)
    language: Mapped[Language] = mapped_column(Enum(Language), nullable=False)
    published_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    is_direct_mention: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    sentiment_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    relevance_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    urgency_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    impact_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    overall_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    status: Mapped[NewsStatus] = mapped_column(Enum(NewsStatus), nullable=False, default=NewsStatus.PENDING)
    operator_rating: Mapped[int | None] = mapped_column(Integer, nullable=True)
    operator_notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    trace_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)
    prompt_version: Mapped[str | None] = mapped_column(String(64), nullable=True)
    model_version: Mapped[str | None] = mapped_column(String(64), nullable=True)

    source = relationship("NewsSource", back_populates="news_items")
