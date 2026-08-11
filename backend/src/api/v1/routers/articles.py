from fastapi import APIRouter, Depends, Query, Path, HTTPException, status
from typing import List, Optional
from uuid import UUID
from backend.src.schemas import ArticleCreate
from backend.src.services.article_service import ArticleService
from backend.src.core.security import get_current_user
from backend.src.models.entities import EditorialStatus
from pydantic import BaseModel

router = APIRouter(prefix="/articles", tags=["Articles"])


class ArticleSearchResponse(BaseModel):
    articles: List[dict]
    total: int


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_article(article: ArticleCreate, user_id: UUID = Depends(get_current_user)):
    service = ArticleService()
    created = await service.create_article(article)
    return created


@router.get("/{article_id}")
async def read_article(article_id: UUID, user_id: UUID = Depends(get_current_user)):
    service = ArticleService()
    article = await service.get_article(article_id)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    return article


@router.put("/{article_id}")
async def update_article(article_id: UUID, article_update: ArticleCreate, user_id: UUID = Depends(get_current_user)):
    service = ArticleService()
    updated = await service.update_article(article_id, article_update)
    if not updated:
        raise HTTPException(status_code=404, detail="Article not found")
    return updated


@router.delete("/{article_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_article(article_id: UUID, user_id: UUID = Depends(get_current_user)):
    service = ArticleService()
    deleted = await service.delete_article(article_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Article not found")
    return None


@router.get("/search", response_model=ArticleSearchResponse)
async def search_articles(
    query: Optional[str] = Query(None, min_length=3, max_length=100),
    country: Optional[str] = Query(None),
    language: Optional[str] = Query(None),
    entities: Optional[List[str]] = Query(None),
    categories: Optional[List[str]] = Query(None),
    keywords: Optional[List[str]] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    user_id: UUID = Depends(get_current_user)
):
    service = ArticleService()
    results, total = await service.search_articles(
        query=query,
        country=country,
        language=language,
        entities=entities or [],
        categories=categories or [],
        keywords=keywords or [],
        skip=skip,
        limit=limit
    )
    return ArticleSearchResponse(articles=results, total=total)


class ArticleRateRequest(BaseModel):
    rating: int
    feedback: Optional[str] = None
    status: Optional[EditorialStatus] = None


@router.post("/{article_id}/rate")
async def rate_article(article_id: UUID, rate_request: ArticleRateRequest, user_id: UUID = Depends(get_current_user)):
    service = ArticleService()
    updated = await service.rate_article(article_id, user_id, rate_request.rating, rate_request.feedback, rate_request.status)
    if not updated:
        raise HTTPException(status_code=404, detail="Article not found")
    return updated
