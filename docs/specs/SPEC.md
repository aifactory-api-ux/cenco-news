# SPEC.md

## CENCO NEWS - Technical Specification

---

## 1. TECHNOLOGY STACK

### Backend
| Component | Technology | Version |
|---|---|---|
| Language | Python | 3.11+ |
| Web Framework | FastAPI | 0.109.0 |
| ORM | SQLAlchemy | 2.0.25 |
| Database | PostgreSQL | 15+ |
| Cache | Redis | 7.2+ |
| Async HTTP Client | httpx | 0.26.0 |
| PDF Generation | WeasyPrint | 60.2 |
| HTML Template Engine | Jinja2 | 3.1.3 |
| RSS Parsing | feedparser | 6.0.10 |
| HTML Scraping | Beautiful Soup | 4.12.3 |
| Data Validation | Pydantic | 2.5.3 |
| Prometheus Metrics | prometheus-client | 0.19.0 |
| Distributed Tracing | opentelemetry-api | 1.22.0 |
| Password Hashing | passlib | 1.7.4 |
| JWT Handling | python-jose | 3.3.0 |
| CORS | fastapi-cors | 0.0.1 |
| Background Tasks | celery | 5.3.6 |
| Celery Broker | redis | (same as cache) |
| Environment Config | pydantic-settings | 2.1.0 |
| UUID Generation | uuid | (stdlib) |
| Date/Time | datetime | (stdlib) |

### Frontend
| Component | Technology | Version |
|---|---|---|
| Language | TypeScript | 5.3+ |
| Build Tool | Vite | 5.1.0 |
| UI Framework | React | 18.2.0 |
| Routing | react-router-dom | 6.22.0 |
| HTTP Client | axios | 1.6.7 |
| State Management | zustand | 4.5.1 |
| CSS | Tailwind CSS | 3.4.1 |
| Icons | lucide-react | 0.330.0 |
| Date Handling | date-fns | 3.3.1 |
| Form Validation | react-hook-form | 7.50.1 |
| Charts | recharts | 2.10.4 |
| React Query | @tanstack/react-query | 5.17.19 |

### Infrastructure
| Component | Technology |
|---|---|
| Containerization | Docker, Docker Compose |
| Process Manager | Celery |
| Message Broker | Redis |
| Monitoring | Prometheus, Grafana |
| Cloud Provider | AWS (configurable) |

---

## 2. DATA CONTRACTS

### Python Pydantic Models (Backend)

```python
# shared/models/user.py
from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from datetime import datetime
from uuid import UUID
from enum import Enum

class UserRole(str, Enum):
    ADMIN = "admin"
    MANAGER = "manager"
    NEWS_OPERATOR = "news_operator"
    VIEWER = "viewer"

class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    role: UserRole

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None

class User(UserBase):
    id: UUID
    is_active: bool
    created_at: datetime
    updated_at: datetime
    last_login: Optional[datetime] = None

    class Config:
        from_attributes = True

class UserInDB(User):
    hashed_password: str

# shared/models/news.py
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from uuid import UUID
from enum import Enum

class NewsSourceType(str, Enum):
    RSS = "rss"
    WEB_SCRAPE = "web_scrape"
    NEWS_API = "news_api"

class NewsStatus(str, Enum):
    PENDING = "pending"
    REVIEWED = "reviewed"
    APPROVED = "approved"
    REJECTED = "rejected"
    PUBLISHED = "published"

class Language(str, Enum):
    SPANISH = "es"
    PORTUGUESE = "pt"
    ENGLISH = "en"

class Country(str, Enum):
    CHILE = "chile"
    ARGENTINA = "argentina"
    BRAZIL = "brazil"
    PERU = "peru"
    COLOMBIA = "colombia"
    URUGUAY = "uruguay"

class NewsSourceBase(BaseModel):
    name: str
    source_type: NewsSourceType
    url: str
    is_active: bool = True
    country: Optional[Country] = None
    language: Optional[Language] = None
    scrape_pattern: Optional[str] = None
    polling_interval_minutes: int = 60

class NewsSourceCreate(NewsSourceBase):
    pass

class NewsSource(NewsSourceBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class NewsItemBase(BaseModel):
    title: str
    content_summary: Optional[str] = None
    full_content: Optional[str] = None
    url: str
    source_id: UUID
    country: Country
    language: Language
    published_at: Optional[datetime] = None
    is_direct_mention: bool = False
    sentiment_score: Optional[float] = None

class NewsItemCreate(NewsItemBase):
    source_name: Optional[str] = None
    image_url: Optional[str] = None
    trace_id: UUID

class NewsItem(NewsItemBase):
    id: UUID
    relevance_score: float = 0.0
    urgency_score: float = 0.0
    impact_score: float = 0.0
    overall_score: float = 0.0
    status: NewsStatus = NewsStatus.PENDING
    operator_rating: Optional[int] = None
    operator_notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    trace_id: UUID
    prompt_version: Optional[str] = None
    model_version: Optional[str] = None

    class Config:
        from_attributes = True

class NewsItemWithSource(NewsItem):
    source: NewsSource

class NewsItemFilter(BaseModel):
    status: Optional[NewsStatus] = None
    source_id: Optional[UUID] = None
    country: Optional[Country] = None
    language: Optional[Language] = None
    is_direct_mention: Optional[bool] = None
    min_score: Optional[float] = None
    max_score: Optional[float] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    search_query: Optional[str] = None

class NewsItemListResponse(BaseModel):
    items: List[NewsItemWithSource]
    total: int
    page: int
    page_size: int
    pages: int

# shared/models/scoring.py
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from uuid import UUID

class ScoringDimensionBase(BaseModel):
    name: str
    description: str
    weight: float = Field(ge=0, le=1)
    is_active: bool = True

class ScoringDimensionCreate(ScoringDimensionBase):
    pass

class ScoringDimension(ScoringDimensionBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ScoringWeights(BaseModel):
    relevance_weight: float = Field(default=0.33, ge=0, le=1)
    urgency_weight: float = Field(default=0.33, ge=0, le=1)
    impact_weight: float = Field(default=0.34, ge=0, le=1)

class ScoringResult(BaseModel):
    news_id: UUID
    relevance_score: float
    urgency_score: float
    impact_score: float
    overall_score: float
    explanation: Dict[str, Any]
    prompt_version: str
    model_version: str
    calculated_at: datetime

# shared/models/report.py
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from uuid import UUID
from enum import Enum

class ReportStatus(str, Enum):
    DRAFT = "draft"
    PENDING_APPROVAL = "pending_approval"
    APPROVED = "approved"
    REJECTED = "rejected"
    PUBLISHED = "published"
    SENT = "sent"

class ReportFormat(str, Enum):
    PDF = "pdf"
    HTML = "html"
    CSV = "csv"

class ReportTemplateBase(BaseModel):
    name: str
    description: Optional[str] = None
    template_content: str
    is_active: bool = True

class ReportTemplateCreate(ReportTemplateBase):
    pass

class ReportTemplate(ReportTemplateBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ReportBase(BaseModel):
    title: str
    template_id: Optional[UUID] = None
    country_filter: Optional[str] = None
    language_filter: Optional[str] = None
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None
    min_score: Optional[float] = None
    status: ReportStatus = ReportStatus.DRAFT

class ReportCreate(ReportBase):
    include_news_ids: List[UUID] = []

class Report(ReportBase):
    id: UUID
    content_html: Optional[str] = None
    approved_by: Optional[UUID] = None
    approved_at: Optional[datetime] = None
    published_at: Optional[datetime] = None
    created_by: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ReportWithNews(Report):
    news_items: List[NewsItem]

# shared/models/notification.py
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from uuid import UUID
from enum import Enum

class ChannelType(str, Enum):
    EMAIL = "email"
    SLACK = "slack"
    WEBHOOK = "webhook"

class NotificationRecipientBase(BaseModel):
    name: str
    email: Optional[str] = None
    slack_webhook: Optional[str] = None
    webhook_url: Optional[str] = None
    is_active: bool = True

class NotificationRecipientCreate(NotificationRecipientBase):
    pass

class NotificationRecipient(NotificationRecipientBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ChannelConfigBase(BaseModel):
    name: str
    channel_type: ChannelType
    is_active: bool = True
    config_data: dict = {}

class ChannelConfigCreate(ChannelConfigBase):
    pass

class ChannelConfig(ChannelConfigBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# shared/models/prompt.py
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from uuid import UUID

class PromptBase(BaseModel):
    name: str
    description: Optional[str] = None
    prompt_template: str
    version: str
    is_active: bool = True

class PromptCreate(PromptBase):
    pass

class Prompt(PromptBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# shared/models/audit.py
from pydantic import BaseModel
from typing import Optional, Any, Dict
from datetime import datetime
from uuid import UUID

class AuditLogBase(BaseModel):
    user_id: UUID
    action: str
    resource_type: str
    resource_id: Optional[UUID] = None
    details: Optional[Dict[str, Any]] = None
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None

class AuditLogCreate(AuditLogBase):
    pass

class AuditLog(AuditLogBase):
    id: UUID
    created_at: datetime

    class Config:
        from_attributes = True

class AuditLogFilter(BaseModel):
    user_id: Optional[UUID] = None
    action: Optional[str] = None
    resource_type: Optional[str] = None
    resource_id: Optional[UUID] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None

class AuditLogListResponse(BaseModel):
    items: List[AuditLog]
    total: int
    page: int
    page_size: int
    pages: int
```

### TypeScript Interfaces (Frontend)

```typescript
// src/types/user.ts
export type UserRole = 'admin' | 'manager' | 'news_operator' | 'viewer';

export