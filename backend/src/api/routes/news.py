from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from backend.src.api.deps import current_user, get_pagination, require_roles_dependency, get_db_session
from backend.src.models.news import NewsStatus
from backend.src.schemas.news_schemas import NewsItemCreate, NewsItemUpdateStatus, NewsItemRateRequest, NewsItemListResponse, NewsItem
from backend.src.services.news_service import NewsService

router = APIRouter()


@router.get("/news", response_model=NewsItemListResponse)
async def list_news(
    page: int = Depends(get_pagination),
    page_size: int = Depends(get_pagination),
    status: NewsStatus | None = None,
    source_id: UUID | None = None,
    country: str | None = None,
    language: str | None = None,
    is_direct_mention: bool | None = None,
    min_score: float | None = None,
    max_score: float | None = None,
    start_date: str | None = None,
    end_date: str | None = None,
    search_query: str | None = None,
    db: AsyncSession = Depends(get_db_session),
    user=Depends(current_user),
):
    news_service = NewsService(db)
    result = await news_service.get_news(
        page=page,
        page_size=page_size,
        status=status,
        source_id=source_id,
        country=country,
        language=language,
        is_direct_mention=is_direct_mention,
        min_score=min_score,
        max_score=max_score,
        start_date=start_date,
        end_date=end_date,
        search_query=search_query,
    )
    return result


@router.post("/news", response_model=NewsItem)
async def create_news(
    news_create: NewsItemCreate,
    db: AsyncSession = Depends(get_db_session),
    user=Depends(require_roles_dependency("admin", "manager", "news_operator")),
):
    news_service = NewsService(db)
    news = await news_service.create_news(news_create)
    return news


@router.get("/news/{news_id}", response_model=NewsItem)
async def get_news(
    news_id: UUID,
    db: AsyncSession = Depends(get_db_session),
    user=Depends(current_user),
):
    news_service = NewsService(db)
    news = await news_service.get_news_by_id(news_id)
    if not news:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Noticia no encontrada")
    return news


@router.patch("/news/{news_id}/status", response_model=NewsItem)
async def update_news_status(
    news_id: UUID,
    status_update: NewsItemUpdateStatus,
    db: AsyncSession = Depends(get_db_session),
    user=Depends(require_roles_dependency("admin", "manager")),
):
    news_service = NewsService(db)
    news = await news_service.update_status(news_id, status_update.status)
    if not news:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Noticia no encontrada")
    return news


@router.post("/news/{news_id}/rate", response_model=NewsItem)
async def rate_news(
    news_id: UUID,
    rate_request: NewsItemRateRequest,
    db: AsyncSession = Depends(get_db_session),
    user=Depends(require_roles_dependency("admin", "manager", "news_operator")),
):
    news_service = NewsService(db)
    news = await news_service.rate_news(news_id, rate_request.rating, rate_request.notes)
    if not news:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Noticia no encontrada")
    return news
