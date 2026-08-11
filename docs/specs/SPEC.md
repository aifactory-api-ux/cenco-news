```markdown
# SPEC.md - CENCO NEWS Project Technical Specification

## 1. TECHNOLOGY STACK

### Backend Technologies
| Technology | Version | Purpose |
|---|---|---|
| Python | 3.11+ | Primary backend language |
| FastAPI | 0.104+ | REST API framework |
| Pydantic | 2.5+ | Data validation and serialization |
| SQLAlchemy | 2.0+ | ORM for PostgreSQL |
| Alembic | 1.13+ | Database migrations |
| PostgreSQL | 15+ | Primary relational database |
| Redis | 7.0+ | Caching and message queuing |
| Qdrant | 1.7+ | Vector database for semantic search |
| RabbitMQ | 3.12+ | Message broker for async processing |
| Celery | 5.3+ | Distributed task queue |
| WeasyPrint | 57+ | PDF generation |
| python-docx | 1.1+ | Word document generation |
| Jinja2 | 3.1+ | HTML templating |
| OpenAI | 1.0+ | LLM API client (or compatible) |
| SpeechRecognition | 3.10+ | Speech-to-text |
| gTTS | 2.4+ | Text-to-speech |
| prometheus-client | 0.19+ | Metrics exposition |
| structlog | 23.2+ | Structured logging |
| opentelemetry-api | 1.22+ | Distributed tracing |
| opentelemetry-sdk | 1.22+ | Tracing SDK |
| python-jose | 3.3+ | JWT token handling |
| passlib | 1.7+ | Password hashing |
| boto3 | 1.34+ | S3 compatible storage |
| httpx | 0.26+ | HTTP client |
| feedparser | 6.0+ | RSS/Atom feed parsing |
| BeautifulSoup | 4.12+ | HTML scraping |

### Frontend Technologies
| Technology | Version | Purpose |
|---|---|---|
| TypeScript | 5.3+ | Type-safe frontend language |
| React | 18.2+ | UI framework |
| Vite | 5.0+ | Build tool and dev server |
| react-router-dom | 6.21+ | Client-side routing |
| @tanstack/react-query | 5.17+ | Server state management |
| Zustand | 4.4+ | Client state management |
| tailwindcss | 3.4+ | Utility CSS framework |
| date-fns | 3.2+ | Date manipulation |
| react-hook-form | 7.49+ | Form handling |
| zod | 3.22+ | Schema validation |
| @headlessui/react | 1.7+ | Accessible UI components |
| lucide-react | 0.303+ | Icon library |
| recharts | 2.10+ | Charts and visualizations |

### Infrastructure Technologies
| Technology | Purpose |
|---|---|
| Kubernetes | Container orchestration |
| Terraform | Infrastructure as Code |
| Docker | Containerization |
| Prometheus | Metrics collection |
| Grafana | Metrics visualization |
| Loki | Log aggregation |
| S3 Compatible Storage | File storage (reports, attachments) |

---

## 2. DATA CONTRACTS

### 2.1 Core Domain Models

#### NewsArticle (Pydantic)
```python
class NewsArticle(BaseModel):
    id: UUID
    trace_id: UUID
    source_id: UUID
    source_name: str
    source_type: SourceType
    url: HttpUrl
    title: str
    content: str
    summary: Optional[str] = None
    author: Optional[str] = None
    published_at: datetime
    fetched_at: datetime
    country: str
    language: Language
    entities: List[str] = []
    categories: List[str] = []
    keywords: List[str] = []
    
    # Scoring fields
    relevance_score: float = 0.0  # 0-33 scale
    urgency_score: float = 0.0    # 0-33 scale
    impact_score: float = 0.0     # 0-33 scale
    overall_score: float = 0.0    # 0-100 scale
    
    # Duplicate detection
    duplicate_group_id: Optional[UUID] = None
    is_duplicate: bool = False
    duplicate_of_id: Optional[UUID] = None
    
    # Editorial workflow
    status: EditorialStatus = EditorialStatus.PENDING
    editor_rating: Optional[int] = None  # 1-5 stars
    editor_feedback: Optional[str] = None
    approved_by: Optional[UUID] = None
    approved_at: Optional[datetime] = None
    
    # Metadata
    prompt_version: str
    model_version: str
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None

class NewsArticleCreate(BaseModel):
    source_id: UUID
    url: HttpUrl
    title: str
    content: str
    summary: Optional[str] = None
    author: Optional[str] = None
    published_at: datetime
    country: str
    language: Language
    entities: List[str] = []
    categories: List[str] = []
    keywords: List[str] = []
    trace_id: Optional[UUID] = None

class NewsArticleUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    summary: Optional[str] = None
    entities: Optional[List[str]] = None
    categories: Optional[List[str]] = None
    keywords: Optional[List[str]] = None
    editor_rating: Optional[int] = None
    editor_feedback: Optional[str] = None
    status: Optional[EditorialStatus] = None

class NewsArticleResponse(BaseModel):
    id: UUID
    trace_id: UUID
    source_name: str
    source_type: SourceType
    url: str
    title: str
    content: str
    summary: Optional[str]
    author: Optional[str]
    published_at: datetime
    country: str
    language: Language
    entities: List[str]
    categories: List[str]
    relevance_score: float
    urgency_score: float
    impact_score: float
    overall_score: float
    duplicate_group_id: Optional[UUID]
    is_duplicate: bool
    status: EditorialStatus
    editor_rating: Optional[int]
    editor_feedback: Optional[str]
    created_at: datetime
```

#### Source (Pydantic)
```python
class SourceType(str, Enum):
    RSS = "rss"
    API = "api"
    SCRAPER = "scraper"

class SourceStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    ERROR = "error"
    MAINTENANCE = "maintenance"

class Source(BaseModel):
    id: UUID
    name: str
    type: SourceType
    url: HttpUrl
    priority: int = 1  # 1-5 scale
    country: str
    language: Language
    status: SourceStatus
    adapter_config: Dict[str, Any] = {}
    last_fetch_at: Optional[datetime] = None
    last_error: Optional[str] = None
    error_count: int = 0
    is_enabled: bool = True
    created_at: datetime
    updated_at: datetime

class SourceCreate(BaseModel):
    name: str
    type: SourceType
    url: HttpUrl
    priority: int = 1
    country: str
    language: Language
    adapter_config: Dict[str, Any] = {}
    is_enabled: bool = True

class SourceUpdate(BaseModel):
    name: Optional[str] = None
    url: Optional[HttpUrl] = None
    priority: Optional[int] = None
    status: Optional[SourceStatus] = None
    adapter_config: Optional[Dict[str, Any]] = None
    is_enabled: Optional[bool] = None
```

#### ScoringConfig (Pydantic)
```python
class ScoringDimension(str, Enum):
    RELEVANCE = "relevance"
    URGENCY = "urgency"
    IMPACT = "impact"

class ScoringRule(BaseModel):
    id: UUID
    dimension: ScoringDimension
    name: str
    description: str
    condition: str  # JSON logic expression
    weight: float = 1.0
    threshold: float = 0.0
    is_enabled: bool = True
    created_at: datetime
    updated_at: datetime

class ScoringCategory(BaseModel):
    id: UUID
    name: str
    keywords: List[str] = []
    weight: float = 1.0
    is_enabled: bool = True

class ScoringConfig(BaseModel):
    id: UUID
    name: str
    description: Optional[str]
    rules: List[ScoringRule] = []
    categories: List[ScoringCategory] = []
    whitelist_entities: List[str] = []
    blacklist_entities: List[str] = []
    relevance_weight: float = 0.33
    urgency_weight: float = 0.33
    impact_weight: float = 0.33
    min_score_threshold: float = 50.0
    is_active: bool = True
    created_at: datetime
    updated_at: datetime

class ScoringConfigUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    rules: Optional[List[ScoringRule]] = None
    categories: Optional[List[ScoringCategory]] = None
    whitelist_entities: Optional[List[str]] = None
    blacklist_entities: Optional[List[str]] = None
    relevance_weight: Optional[float] = None
    urgency_weight: Optional[float] = None
    impact_weight: Optional[float] = None
    min_score_threshold: Optional[float] = None
    is_active: Optional[bool] = None
```

#### Prompt (Pydantic)
```python
class PromptTemplate(BaseModel):
    id: UUID
    name: str
    version: str
    template_type: PromptType
    content: str
    variables: List[str] = []
    description: Optional[str] = None
    is_active: bool = False
    created_by: UUID
    created_at: datetime
    updated_at: datetime

class PromptType(str, Enum):
    SUMMARIZATION = "summarization"
    SCORING = "scoring"
    ENTITY_EXTRACTION = "entity_extraction"
    CATEGORY_CLASSIFICATION = "category_classification"
    DUPLICATE_DETECTION = "duplicate_detection"
    REPORT_GENERATION = "report_generation"
    TRANSLATION = "translation"

class PromptVersionHistory(BaseModel):
    id: UUID
    prompt_id: UUID
    version: str
    content: str
    changed_by: UUID
    change_reason: Optional[str] = None
    created_at: datetime

class PromptSimulationRequest(BaseModel):
    prompt_id: UUID
    variables: Dict[str, str]
    expected_output: Optional[str] = None

class PromptSimulationResponse(BaseModel):
    prompt_id: UUID
    version: str
    rendered_prompt: str
    model_output: str
    execution_time_ms: int
    tokens_used: int
```

#### Report (Pydantic)
```python
class ReportStatus(str, Enum):
    DRAFT = "draft"
    REVIEW = "review"
    APPROVED = "approved"
    PUBLISHED = "published"
    DISTRIBUTED = "distributed"

class Report(BaseModel):
    id: UUID
    title: str
    country: str
    business_unit: str
    language: Language
    status: ReportStatus
    date_range_start: date
    date_range_end: date
    articles: List[UUID] = []
    summary: Optional[str] = None
    generated_at: datetime
    published_at: Optional[datetime] = None
    distributed_at: Optional[datetime] = None
    prompt_version: str
    model_version: str
    trace_id: UUID
    created_by: UUID
    approved_by: Optional[UUID] = None
    approved_at: Optional[datetime] = None
    revision_history: List[ReportRevision] = []
    created_at: datetime
    updated_at: datetime

class ReportRevision(BaseModel):
    id: UUID
    report_id: UUID
    revision_number: int
    changes_description: str
    changed_by: UUID
    created_at: datetime

class ReportCreate(BaseModel):
    title: str
    country: str
    business_unit: str
    language: Language
    date_range_start: date
    date_range_end: date
    article_ids: List[UUID] = []

class ReportGenerateRequest(BaseModel):
    country: str
    business_unit: str
    language: Language
    date_range_start: date
    date_range_end: date
    include_articles: Optional[List[UUID]] = None
    exclude_articles: Optional[List[UUID]] = None

class ReportExportFormat(str, Enum):
    HTML = "html"
    PDF = "pdf"
    WORD = "word"
    CSV = "csv"
```

#### Template (Pydantic)
```python
class Template(BaseModel):
    id: UUID
    name: str
    business_unit: str
    language: Language
    template_type: ReportExportFormat
    content: str  # HTML template content
    css_styles: Optional[str] = None
    is_default: bool = False
    created_at: datetime
    updated_at: datetime

class TemplateCreate(BaseModel):
    name: str
    business_unit: str
    language: Language
    template_type: ReportExportFormat
    content: str
    css_styles: Optional[str] = None
    is_default: bool = False
```

#### Recipient (Pydantic)
```python
class Recipient(BaseModel):
    id: UUID
    email: EmailStr
    name: str
    business_unit: str
    country: Optional[str] = None
    language: Language
    distribution_list_id: UUID
    is_active: bool = True
    created_at: datetime
    updated_at: datetime

class DistributionList(BaseModel):
    id: UUID
    name: str
    description: Optional[str] = None
    business_unit: str
    country: Optional[str] = None
    recipients: List[Recipient] = []
    created_at: datetime
    updated_at: datetime

class DistributionListCreate(BaseModel):
    name: str
    description: Optional[str] = None
    business_unit: str
    country: Optional[str] = None

class RecipientCreate(BaseModel):
    email: EmailStr
    name: str
    business_unit: str
    country: Optional[str] = None
    language: Language
    distribution_list_id: UUID
```

#### User and Authentication
```python
class UserRole(str, Enum):
    ADMIN = "admin"
    EDITOR = "editor"
    VIEWER = "viewer"
    VOICE_USER = "voice_user"

class User(BaseModel):
    id: UUID
    email: EmailStr
    name: str
    role: UserRole
    business_unit: Optional[str] = None
    country: Optional[str] = None
    language_preference: Language = Language.ES
    is_active: bool = True
    last_login_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

class UserCreate(BaseModel):
    email: EmailStr
    name: str
    role: UserRole = UserRole.VIEWER
    business_unit: Optional[str] = None
    country: Optional[str] = None
    language_preference: Language = Language.ES
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user: User
```

#### Audit and Logging
```python
class AuditEvent(BaseModel):
    id: UUID
    event_type: AuditEventType
    entity_type: str
    entity_id: UUID
    user_id: Optional[UUID] = None
    action: str
    changes: Optional[Dict[str, Any]] = None
    old_values: Optional[Dict[str, Any]] = None
    new_values: Optional[