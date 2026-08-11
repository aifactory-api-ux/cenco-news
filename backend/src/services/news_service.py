from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import and_, or_
from typing import Optional
from uuid import UUID
from datetime import datetime
from backend.src.models.news import NewsItem, NewsStatus
from backend.src.schemas.news_schemas import NewsItemCreate
from sqlalchemy.orm import selectinload

class NewsService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_news(
        self,
        page: int = 1,
        page_size: int = 20,
        status: Optional[NewsStatus] = None,
        source_id: Optional[UUID] = None,
        country: Optional[str] = None,
        language: Optional[str] = None,
        is_direct_mention: Optional[bool] = None,
        min_score: Optional[float] = None,
        max_score: Optional[float] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        search_query: Optional[str] = None,
    ):
        query = select(NewsItem).options(selectinload(NewsItem.source))

        filters = []
        if status:
            filters.append(NewsItem.status == status)
        if source_id:
            filters.append(NewsItem.source_id == source_id)
        if country:
            filters.append(NewsItem.country == country)
        if language:
            filters.append(NewsItem.language == language)
        if is_direct_mention is not None:
            filters.append(NewsItem.is_direct_mention == is_direct_mention)
        if min_score is not None:
            filters.append(NewsItem.overall_score >= min_score)
        if max_score is not None:
            filters.append(NewsItem.overall_score <= max_score)
        if start_date:
            try:
                start_dt = datetime.fromisoformat(start_date)
                filters.append(NewsItem.published_at >= start_dt)
            except Exception:
                pass
        if end_date:
            try:
                end_dt = datetime.fromisoformat(end_date)
                filters.append(NewsItem.published_at <= end_dt)
            except Exception:
                pass
        if search_query:
            search_filter = or_(
                NewsItem.title.ilike(f"%{search_query}%"),
                NewsItem.content_summary.ilike(f"%{search_query}%"),
                NewsItem.operator_notes.ilike(f"%{search_query}%"),
            )
            filters.append(search_filter)

        if filters:
            query = query.where(and_(*filters))

        count_query = select(NewsItem).where(and_(*filters)) if filters else select(NewsItem)
        total = await self.db.scalar(count_query.alias().count())

        query = query.offset((page - 1) * page_size).limit(page_size)

        result = await self.db.execute(query)
        items = result.scalars().all()

        pages = (total + page_size - 1) // page_size

        # Map full items to response schema
        return {
            "items": items,
            "total": total,
            "page": page,
            "page_size": page_size,
            "pages": pages,
        }

    async def create_news(self, news_create: NewsItemCreate) -> NewsItem:
        news_item = NewsItem(**news_create.dict(exclude_unset=True))
        self.db.add(news_item)
        await self.db.commit()
        await self.db.refresh(news_item)
        return news_item

    async def get_news_by_id(self, news_id: UUID) -> NewsItem | None:
        query = select(NewsItem).where(NewsItem.id == news_id).options(selectinload(NewsItem.source))
        result = await self.db.execute(query)
        news = result.scalars().first()
        return news

    async def update_status(self, news_id: UUID, status: NewsStatus) -> NewsItem | None:
        query = select(NewsItem).where(NewsItem.id == news_id)
        result = await self.db.execute(query)
        news = result.scalars().first()
        if not news:
            return None
        news.status = status
        await self.db.commit()
        await self.db.refresh(news)
        return news

    async def rate_news(self, news_id: UUID, rating: int, notes: str | None) -> NewsItem | None:
        query = select(NewsItem).where(NewsItem.id == news_id)
        result = await self.db.execute(query)
        news = result.scalars().first()
        if not news:
            return None
        news.operator_rating = rating
        news.operator_notes = notes
        await self.db.commit()
        await self.db.refresh(news)
        return news
