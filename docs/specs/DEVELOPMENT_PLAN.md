# DEVELOPMENT PLAN: CENCO NEWS

## 1. ARCHITECTURE OVERVIEW

### System Context
CENCO NEWS es una plataforma de inteligencia de noticias para Cencosud que automatiza la captura, clasificación, puntuación, síntesis, aprobación y distribución de noticias desde múltiples fuentes (RSS, Web Scraping, News APIs). El sistema utiliza FastAPI como API Gateway/backend unificado, PostgreSQL como base de datos, Redis para caché y Celery para tareas asíncronas.

### Technology Stack
- **Backend:** Python 3.11+, FastAPI 0.109.0, SQLAlchemy 2.0.25, Alembic
- **Frontend:** TypeScript 5.3+, React 18.2.0, Vite 5.1.0, Tailwind CSS 3.4.1, React Router 6
- **Database:** PostgreSQL 15+, Redis 7.2+
- **Async Tasks:** Celery 5.3.6
- **PDF Generation:** WeasyPrint 60.2
- **Containerization:** Docker, Docker Compose

### Folder Structure
```
cenco-news/
├── frontend/                    → React SPA
│   ├── src/
│   │   ├── components/ui/       → Base components
│   │   ├── pages/               → Page components
│   │   ├── hooks/               → Custom hooks
│   │   ├── services/           → API services
│   │   ├── stores/              → Zustand stores
│   │   └── styles/              → Design tokens
│   └── Dockerfile
├── backend/
│   ├── src/
│   │   ├── api/                → API routes
│   │   ├── models/              → SQLAlchemy models
│   │   ├── schemas/             → Pydantic schemas
│   │   ├── services/            → Business logic
│   │   ├── tasks/               → Celery tasks
│   │   ├── core/                → Config, security
│   │   └── main.py              → FastAPI app
│   ├── alembic/                 → DB migrations
│   └── Dockerfile
├── shared/
│   └── types.ts                → TypeScript shared types
├── docker-compose.yml
├── run.sh
└── .env.example
```

### Database Schema
- **users** - User accounts with roles (admin, manager, news_operator, viewer)
- **news_sources** - RSS, web scraping, and API source configurations
- **news_items** - Collected news with scoring and status
- **scoring_dimensions** - Configurable scoring weights
- **reports** - Generated reports with templates
- **report_templates** - Report template definitions
- **notification_recipients** - Email, Slack, webhook recipients
- **channel_configs** - Notification channel settings
- **prompts** - AI prompt templates
- **audit_logs** - User action audit trail

### API Endpoints (per SPEC.md §3)
- `POST/GET /api/v1/auth/login` - Authentication
- `GET/POST /api/v1/news` - News CRUD and search
- `GET /api/v1/news/{id}` - News detail
- `PATCH /api/v1/news/{id}/status` - Update news status
- `POST /api/v1/news/{id}/rate` - Rate news
- `GET/POST /api/v1/sources` - News sources management
- `GET/POST /api/v1/scoring/dimensions` - Scoring dimensions
- `POST /api/v1/scoring/calculate/{news_id}` - Calculate news score
- `GET/POST /api/v1/reports` - Report management
- `GET/POST /api/v1/reports/{id}/approve` - Approve reports
- `POST /api/v1/reports/{id}/send` - Send reports
- `GET /api/v1/reports/templates` - Report templates
- `GET/POST /api/v1/notifications/recipients` - Notification recipients
- `GET/POST /api/v1/notifications/channels` - Channel configs
- `GET/POST /api/v1/prompts` - Prompt templates
- `GET /api/v1/audit` - Audit logs
- `GET /health` - Health check

---

## 2. ACCEPTANCE CRITERIA

1. **Autenticación:** Usuarios pueden iniciar sesión con email/password y recibir JWT token válido
2. **Dashboard Daily Pulse:** Muestra resumen de noticias del día con métricas y noticias destacadas
3. **Detalle de Noticia:** Vista completa de noticia con título, contenido, fuente, scores y calificación
4. **Búsqueda e Histórico:** Filtrado por estado, país, idioma, fuente, rango de fechas y score
5. **Gestión de Fuentes:** CRUD de fuentes RSS, scraping y API con configuración de polling
6. **Scoring Configurable:** Dimensiones de scoring con pesos ajustables
7. **Reportes:** Generación de reportes PDF/HTML con plantillas, aprobación y envío
8. **Notificaciones:** Configuración de canales email/Slack/webhook y destinatarios
9. **Auditoría:** Log completo de acciones de usuarios con filtros
10. **Docker Setup:** `./run.sh` levanta todos los servicios sin pasos manuales

---

## TEAM SCOPE

**Roles assigned:**
- role-tl (technical_lead) - Foundation, Backend API
- role-fe (frontend_developer) - Frontend implementation
- role-devops (devops_support) - Infrastructure & Deployment

---

## 3. EXECUTABLE ITEMS

### ITEM 1: Foundation — shared types, schemas, DB schema, config

**Goal:** Create ALL shared code that backend and frontend will import. This includes TypeScript types, Python Pydantic models, database schema, configuration, and utility functions. This item establishes the contract between frontend and backend.

**Files to create:**
- shared/types.ts (create) - All TypeScript interfaces, enums, and shared types for frontend (UserRole, User, NewsSource, NewsItem, Report, NotificationRecipient, ChannelConfig, Prompt, AuditLog, API responses)
- backend/src/core/config.py (create) - Pydantic settings for environment validation, database URL, JWT secret, Redis config, Celery config, AI service config
- backend/src/core/security.py (create) - JWT token creation/validation, password hashing with passlib, role-based access decorators
- backend/src/models/__init__.py (create) - SQLAlchemy model imports (User, NewsSource, NewsItem, ScoringDimension, Report, ReportTemplate, NotificationRecipient, ChannelConfig, Prompt, AuditLog)
- backend/src/models/user.py (create) - User SQLAlchemy model with all fields from SPEC.md §2
- backend/src/models/news.py (create) - NewsSource and NewsItem SQLAlchemy models
- backend/src/models/scoring.py (create) - ScoringDimension SQLAlchemy model
- backend/src/models/report.py (create) - Report and ReportTemplate SQLAlchemy models
- backend/src/models/notification.py (create) - NotificationRecipient and ChannelConfig models
- backend/src/models/prompt.py (create) - Prompt SQLAlchemy model
- backend/src/models/audit.py (create) - AuditLog SQLAlchemy model
- backend/src/db/database.py (create) - SQLAlchemy engine, session, Base, get_db dependency
- backend/src/db/schema.sql (create) - Complete PostgreSQL schema with all tables, indexes, foreign keys, and seed data (3-5 users, sample sources, sample news items)
- backend/alembic.ini (create) - Alembic configuration for migrations
- backend/alembic/env.py (create) - Alembic environment setup
- backend/alembic/versions/001_initial_schema.py (create) - Initial migration creating all tables
- requirements.txt (create) - All Python dependencies: fastapi==0.109.0, sqlalchemy==2.0.25, pydantic==2.5.3, pydantic-settings==2.1.0, python-jose==3.3.0, passlib==1.7.4, alembic==1.13.1, psycopg2-binary==2.9.9, redis==5.0.1, celery==5.3.6, httpx==0.26.0, beautifulsoup4==4.12.3, feedparser==6.0.10, weasyprint==60.2, jinja2==3.1.3, prometheus-client==0.19.0, python-multipart==0.0.6
- frontend/package.json (create) - All frontend dependencies: react==18.2.0, react-dom==18.2.0, react-router-dom==6.22.0, axios==1.6.7, zustand==4.5.1, @tanstack/react-query==5.17.19, react-hook-form==7.50.1, date-fns==3.3.1, recharts==2.10.4, lucide-react==0.330.0, tailwindcss==3.4.1, @headlessui/react==1.7.18
- frontend/tsconfig.json (create) - TypeScript config with strict mode, path aliases
- frontend/vite.config.ts (create) - Vite config with React plugin, proxy setup
- frontend/tailwind.config.js (create) - Tailwind config with design tokens from UI contract
- frontend/src/styles/tokens.ts (create) - Design tokens verbatim from UIUX contract (colors, typography, spacing, radii, shadows)

**Dependencies:** None

**Validation:** 
- Run `python -c "from backend.src.models import *; from backend.src.core.config import *"` to verify Python imports work
- Run `cd frontend && npx tsc --noEmit` to verify TypeScript compiles without errors

**Role:** role-tl (technical_lead)

---

### ITEM 2: Backend API — authentication, news endpoints, sources management

**Goal:** Implement FastAPI backend with all REST endpoints per SPEC.md §3. This item covers authentication, news CRUD, news sources management, and health check. All endpoints return Pydantic schemas defined in Item 1.

**Files to create:**
- backend/src/main.py (create) - FastAPI app factory with lifespan, CORS, routes registration, middleware for logging and audit
- backend/src/api/__init__.py (create) - API router exports
- backend/src/api/deps.py (create) - Dependencies: get_current_user, require_roles, get_pagination
- backend/src/api/routes/auth.py (create) - POST /api/v1/auth/login, POST /api/v1/auth/refresh
- backend/src/api/routes/news.py (create) - GET/POST /api/v1/news, GET /api/v1/news/{id}, PATCH /api/v1/news/{id}/status, POST /api/v1/news/{id}/rate
- backend/src/api/routes/sources.py (create) - GET/POST /api/v1/sources, GET/PUT/DELETE /api/v1/sources/{id}
- backend/src/api/routes/health.py (create) - GET /health, GET /health/ready
- backend/src/services/user_service.py (create) - User CRUD operations
- backend/src/services/news_service.py (create) - News CRUD, search with filters, pagination
- backend/src/services/source_service.py (create) - News source management
- backend/Dockerfile (create) - Multi-stage Python build, EXPOSE 8000, CMD: uvicorn src.main:app

**Dependencies:** Item 1

**Validation:** 
- Start backend container and verify: `curl http://localhost:8000/health` returns `{"status":"ok"}`
- Test login: `curl -X POST http://localhost:8000/api/v1/auth/login -H "Content-Type: application/json" -d '{"email":"admin@cencosud.com","password":"admin123"}'`

**Role:** role-tl (technical_lead)

---

### ITEM 3: Backend API — scoring, reports, notifications, prompts, audit

**Goal:** Implement remaining backend endpoints: scoring dimensions and calculation, report generation with templates and PDF export, notification channels and recipients, prompt templates, and audit log retrieval.

**Files to create:**
- backend/src/api/routes/scoring.py (create) - GET/POST /api/v1/scoring/dimensions, POST /api/v1/scoring/calculate/{news_id}
- backend/src/api/routes/reports.py (create) - GET/POST /api/v1/reports, GET/PUT/DELETE /api/v1/reports/{id}, POST /api/v1/reports/{id}/approve, POST /api/v1/reports/{id}/send, GET /api/v1/reports/templates
- backend/src/api/routes/notifications.py (create) - GET/POST /api/v1/notifications/recipients, GET/PUT/DELETE /api/v1/notifications/recipients/{id}, GET/POST /api/v1/notifications/channels
- backend/src/api/routes/prompts.py (create) - GET/POST /api/v1/prompts, GET/PUT/DELETE /api/v1/prompts/{id}
- backend/src/api/routes/audit.py (create) - GET /api/v1/audit with filters
- backend/src/services/scoring_service.py (create) - Scoring calculation logic with weighted dimensions
- backend/src/services/report_service.py (create) - Report generation with Jinja2 templates, PDF export with WeasyPrint
- backend/src/services/notification_service.py (create) - Send notifications via email/Slack/webhook
- backend/src/services/prompt_service.py (create) - Prompt template management
- backend/src/services/audit_service.py (create) - Audit log creation and retrieval
- backend/src/tasks/__init__.py (create) - Celery app configuration
- backend/src/tasks/news_tasks.py (create) - Celery tasks for news scraping and processing

**Dependencies:** Item 1

**Validation:** 
- Verify scoring endpoint: `curl -H "Authorization: Bearer <token>" http://localhost:8000/api/v1/scoring/dimensions`
- Verify reports list: `curl -H "Authorization: Bearer <token>" http://localhost:8000/api/v1/reports`

**Role:** role-tl (technical_lead)

---

### ITEM 4: Frontend — foundation, auth flow, layout components

**Goal:** Implement frontend foundation: design tokens, layout with sidebar navigation, auth context/store, API service layer, and login page. This establishes the visual direction per UIUX contract (blue palette, Inter font).

**Files to create:**
- frontend/src/App.tsx (create) - Root component with React Router setup
- frontend/src/main.tsx (create) - Entry point, React Query provider setup
- frontend/src/lib/api.ts (create) - Axios instance with interceptors for auth token
- frontend/src/services/auth.service.ts (create) - Login API calls
- frontend/src/services/news.service.ts (create) - News API calls
- frontend/src/services/sources.service.ts (create) - Sources API calls
- frontend/src/services/reports.service.ts (create) - Reports API calls
- frontend/src/services/scoring.service.ts (create) - Scoring API calls
- frontend/src/services/notifications.service.ts (create) - Notifications API calls
- frontend/src/services/audit.service.ts (create) - Audit API calls
- frontend/src/stores/auth.store.ts (create) - Zustand store for auth state (user, token, role)
- frontend/src/components/ui/Sidebar.tsx (create) - Primary navigation sidebar with menu items per UIUX design
- frontend/src/components/ui/Header.tsx (create) - Top bar with user profile, notifications icon
- frontend/src/components/ui/Button.tsx (create) - Primary CTA button component with variants
- frontend/src/components/ui/Input.tsx (create) - Text input component with label and error state
- frontend/src/components/ui/Select.tsx (create) - Dropdown/select component
- frontend/src/components/ui/Badge.tsx (create) - Status badge component (pending, approved, rejected)
- frontend/src/pages/LoginPage.tsx (create) - Login page with email/password form per Figma login frame
- frontend/Dockerfile (create) - Multi-stage Vite build, nginx serve, EXPOSE 3000