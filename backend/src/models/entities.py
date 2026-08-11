from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, Date, ForeignKey, Text, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declared_attr
from enum import Enum
import uuid
from datetime import datetime


class Language(str, Enum):
    ES = 'es'
    PT = 'pt'
    EN = 'en'

class EditorialStatus(str, Enum):
    PENDING = 'pending'
    APPROVED = 'approved'
    REJECTED = 'rejected'

class SourceType(str, Enum):
    RSS = 'rss'
    API = 'api'
    SCRAPER = 'scraper'

class SourceStatus(str, Enum):
    ACTIVE = 'active'
    INACTIVE = 'inactive'
    ERROR = 'error'
    MAINTENANCE = 'maintenance'

class ReportStatus(str, Enum):
    DRAFT = 'draft'
    PUBLISHED = 'published'
    DISTRIBUTED = 'distributed'


from backend.src.core.database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, nullable=False, index=True)
    name = Column(String, nullable=False)
    role = Column(String, nullable=False)  # UserRole enum string
    business_unit = Column(String, nullable=True)
    country = Column(String, nullable=True)
    language_preference = Column(SQLEnum(Language), nullable=False, default=Language.ES)
    is_active = Column(Boolean, default=True)
    last_login_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class Source(Base):
    __tablename__ = 'sources'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    type = Column(SQLEnum(SourceType), nullable=False)
    url = Column(String, nullable=False)
    priority = Column(Integer, default=1)
    country = Column(String, nullable=False)
    language = Column(SQLEnum(Language), nullable=False)
    status = Column(SQLEnum(SourceStatus), nullable=False, default=SourceStatus.ACTIVE)
    adapter_config = Column(Text, default='{}')
    last_fetch_at = Column(DateTime, nullable=True)
    last_error = Column(String, nullable=True)
    error_count = Column(Integer, default=0)
    is_enabled = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class NewsArticle(Base):
    __tablename__ = 'news_articles'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    trace_id = Column(UUID(as_uuid=True), nullable=False, default=uuid.uuid4)
    source_id = Column(UUID(as_uuid=True), ForeignKey('sources.id'), nullable=False)
    source_name = Column(String, nullable=False)
    source_type = Column(SQLEnum(SourceType), nullable=False)
    url = Column(String, nullable=False)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    summary = Column(Text, nullable=True)
    author = Column(String, nullable=True)
    published_at = Column(DateTime, nullable=False)
    fetched_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    country = Column(String, nullable=False)
    language = Column(SQLEnum(Language), nullable=False)
    entities = Column(Text, nullable=False, default='[]')  # JSON array string
    categories = Column(Text, nullable=False, default='[]')  # JSON array string
    keywords = Column(Text, nullable=False, default='[]')  # JSON array string
    relevance_score = Column(Float, default=0.0)
    urgency_score = Column(Float, default=0.0)
    impact_score = Column(Float, default=0.0)
    overall_score = Column(Float, default=0.0)
    duplicate_group_id = Column(UUID(as_uuid=True), nullable=True)
    is_duplicate = Column(Boolean, default=False)
    duplicate_of_id = Column(UUID(as_uuid=True), nullable=True)
    status = Column(SQLEnum(EditorialStatus), default=EditorialStatus.PENDING, nullable=False)
    editor_rating = Column(Integer, nullable=True)
    editor_feedback = Column(Text, nullable=True)
    approved_by = Column(UUID(as_uuid=True), nullable=True)
    approved_at = Column(DateTime, nullable=True)
    prompt_version = Column(String, nullable=False)
    model_version = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    deleted_at = Column(DateTime, nullable=True)


class ReportRevision(Base):
    __tablename__ = 'report_revisions'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    report_id = Column(UUID(as_uuid=True), ForeignKey('reports.id'))
    revision_number = Column(Integer, nullable=False)
    changes_description = Column(Text, nullable=False)
    changed_by = Column(UUID(as_uuid=True), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class Report(Base):
    __tablename__ = 'reports'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    country = Column(String, nullable=False)
    business_unit = Column(String, nullable=False)
    language = Column(SQLEnum(Language), nullable=False)
    status = Column(SQLEnum(ReportStatus), nullable=False)
    date_range_start = Column(Date, nullable=False)
    date_range_end = Column(Date, nullable=False)
    articles = Column(Text, nullable=False, default='[]')  # JSON array string of UUIDs
    summary = Column(Text, nullable=True)
    generated_at = Column(DateTime, nullable=False)
    published_at = Column(DateTime, nullable=True)
    distributed_at = Column(DateTime, nullable=True)
    prompt_version = Column(String, nullable=False)
    model_version = Column(String, nullable=False)
    trace_id = Column(UUID(as_uuid=True), nullable=False)
    created_by = Column(UUID(as_uuid=True), nullable=False)
    approved_by = Column(UUID(as_uuid=True), nullable=True)
    approved_at = Column(DateTime, nullable=True)
    revision_history = relationship('ReportRevision', backref='report')
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class Template(Base):
    __tablename__ = 'templates'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    business_unit = Column(String, nullable=False)
    language = Column(SQLEnum(Language), nullable=False)
    template_type = Column(String, nullable=False)  # ReportExportFormat string
    content = Column(Text, nullable=False)
    css_styles = Column(Text, nullable=True)
    is_default = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class Recipient(Base):
    __tablename__ = 'recipients'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, nullable=False)
    name = Column(String, nullable=False)
    business_unit = Column(String, nullable=False)
    country = Column(String, nullable=True)
    language = Column(SQLEnum(Language), nullable=False)
    distribution_list_id = Column(UUID(as_uuid=True), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class DistributionList(Base):
    __tablename__ = 'distribution_lists'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    business_unit = Column(String, nullable=False)
    country = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    recipients = relationship('Recipient', backref='distribution_list')


class Approval(Base):
    __tablename__ = 'approvals'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    article_id = Column(UUID(as_uuid=True), nullable=False)
    editor_id = Column(UUID(as_uuid=True), nullable=False)
    rating = Column(Integer, nullable=False)  # 1-5
    feedback = Column(Text, nullable=True)
    status = Column(SQLEnum(EditorialStatus), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class AuditLog(Base):
    __tablename__ = 'audit_logs'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    event_type = Column(String, nullable=False)
    entity_type = Column(String, nullable=False)
    entity_id = Column(UUID(as_uuid=True), nullable=False)
    user_id = Column(UUID(as_uuid=True), nullable=True)
    action = Column(String, nullable=False)
    changes = Column(Text, nullable=True)  # JSON
    old_values = Column(Text, nullable=True)  # JSON
    new_values = Column(Text, nullable=True)  # JSON
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
