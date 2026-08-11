from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.routing import APIRouter
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.base import RequestResponseEndpoint
from typing import Callable
import logging
import uvicorn

from backend.src.api.routes import auth, news, sources, health
from backend.src.api.deps import get_current_user, require_roles


class AuditMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint):
        # Here audit logic can be implemented (skip actual DB logging for this task)
        response = await call_next(request)
        # Add audit headers or logging here if needed
        return response


def create_app() -> FastAPI:
    app = FastAPI(title="CENCO NEWS API", version="1.0.0")

    # Setup CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Add custom audit middleware
    app.add_middleware(AuditMiddleware)

    # Include API routes
    api_router = APIRouter(prefix="/api/v1")

    api_router.include_router(auth.router, tags=["Authentication"])
    api_router.include_router(news.router, tags=["News"])
    api_router.include_router(sources.router, tags=["Sources"])
    api_router.include_router(health.router, tags=["Health"])

    app.include_router(api_router)

    return app


app = create_app()


if __name__ == "__main__":
    uvicorn.run("backend.src.main:app", host="0.0.0.0", port=8000, reload=True)
