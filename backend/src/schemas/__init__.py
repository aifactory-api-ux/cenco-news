from pydantic import BaseModel, EmailStr, HttpUrl
from typing import Optional, List, Dict, Any
from uuid import UUID
from enum import Enum
from datetime import datetime, date
from backend.src.models.entities import EditorialStatus, SourceType, ReportStatus, Language

# User schemas
class UserCreate(BaseModel):
    email: EmailStr
    name: str
    role: str
    business_unit: Optional[str]
    country: Optional[str]
    language_preference: Optional[str]
    password: str

class SourceCreate(BaseModel):
    name: str
    type: str
    url: HttpUrl
    priority: Optional[int] = 1
    country: str
    language: str
    adapter_config: Optional[Dict[str, Any]] = {}
    is_enabled: Optional[bool] = True

class ArticleCreate(BaseModel):
    source_id: UUID
    url: HttpUrl
    title: str
    content: str
    summary: Optional[str] = None
    author: Optional[str] = None
    published_at: datetime
    country: str
    language: str
    entities: List[str] = []
    categories: List[str] = []
    keywords: List[str] = []

class ReportCreate(BaseModel):
    title: str
    country: str
    business_unit: str
    language: str
    date_range_start: date
    date_range_end: date
    article_ids: List[UUID] = []

class ApprovalCreate(BaseModel):
    article_id: UUID
    editor_id: UUID
    rating: int
    feedback: Optional[str]
    status: str
