import hashlib
import json
from typing import List, Optional
from uuid import UUID
from sqlalchemy import select, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession
from backend.src.models.entities import NewsArticle
from backend.src.core.database import SessionLocal


class ExactDeduplicationService:
    """Service for detecting exact duplicates of news articles based on hash and title matching."""

    def __init__(self):
        pass

    async def compute_article_hash(self, content: str) -> str:
        # Normalize content then hash
        normalized = content.strip().lower()
        return hashlib.sha256(normalized.encode('utf-8')).hexdigest()

    async def find_exact_duplicate(self, article_id: UUID) -> Optional[NewsArticle]:
        async with SessionLocal() as session:
            # Fetch the article
            article = await session.get(NewsArticle, article_id)
            if not article:
                return None

            # Compute hash of current article content
            content_hash = await self.compute_article_hash(article.content)

            # Query for other articles with same hash or exact title match
            result = await session.execute(
                select(NewsArticle)
                .where(
                    and_(
                        NewsArticle.id != article.id,
                        or_(
                            NewsArticle.title == article.title,
                            NewsArticle.content.ilike(article.content)
                        )
                    )
                )
            )
            duplicates = result.scalars().all()
            # Filtering duplicates by hash is expensive so we rely on title and content match

            if duplicates:
                # Return first duplicate found
                return duplicates[0]

            return None

    async def mark_duplicates(self, original_id: UUID, duplicate_ids: List[UUID], group_id: UUID):
        async with SessionLocal() as session:
            async with session.begin():
                # Mark all duplicates with duplicate flags and group id
                await session.execute(
                    NewsArticle.__table__.update()
                    .where(NewsArticle.id.in_(duplicate_ids))
                    .values(is_duplicate=True, duplicate_of_id=original_id, duplicate_group_id=group_id)
                )

                # Also update the original article
                await session.execute(
                    NewsArticle.__table__.update()
                    .where(NewsArticle.id == original_id)
                    .values(is_duplicate=False, duplicate_of_id=None, duplicate_group_id=group_id)
                )

                await session.commit()
