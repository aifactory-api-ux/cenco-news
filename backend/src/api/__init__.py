from backend.src.api.routes.auth import router as auth_router
from backend.src.api.routes.news import router as news_router
from backend.src.api.routes.sources import router as sources_router
from backend.src.api.routes.health import router as health_router

__all__ = ["auth_router", "news_router", "sources_router", "health_router"]
