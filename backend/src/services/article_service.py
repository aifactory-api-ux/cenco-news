import json
from typing import Optional, Tuple, List, Any
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update, delete, func
from backend.src.models.entities import NewsArticle
from backend.src.schemas import ArticleCreate
from backend.src.core.database import SessionLocal
from backend.src.services.intelligence.normalizer import normalize_content
from backend.src.services.intelligence.entity_extractor import extract_entities
from backend.src.services.intelligence.classifier import classify_categories
from backend.src.services.intelligence.scoring import calculate_scores
from backend.src.services.intelligence.summarizer import summarize_content

class ArticleService:

    async def create_article(self, article_create: ArticleCreate) -> dict:
        async with SessionLocal() as session:
            async with session.begin():
                normalized_content = normalize_content(article_create.content)
                entities = extract_entities(normalized_content)
                categories = classify_categories(normalized_content)
                relevance, urgency, impact, overall = calculate_scores(article_create, entities, categories)
                summary = summarize_content(normalized_content)

                article = NewsArticle(
                    source_id=article_create.source_id,
                    trace_id=UUID(),
                    source_name="",
                    source_type="rss",
                    url=str(article_create.url),
                    title=article_create.title,
                    content=normalized_content,
                    summary=summary,
                    author=article_create.author,
                    published_at=article_create.published_at,
                    fetched_at=None,
                    country=article_create.country,
                    language=article_create.language,
                    entities=json.dumps(entities),
                    categories=json.dumps(categories),
                    keywords=json.dumps(article_create.keywords),
                    relevance_score=relevance,
                    urgency_score=urgency,
                    impact_score=impact,
                    overall_score=overall,
                    is_duplicate=False,
                    status="pending",
                    prompt_version="v1",
                    model_version="v1",
                    created_at=None,
                    updated_at=None
                )
                session.add(article)
            await session.commit()
            return self._to_dict(article)

    async def get_article(self, article_id: UUID) -> Optional[dict]:
        async with SessionLocal() as session:
            result = await session.execute(select(NewsArticle).filter(NewsArticle.id == article_id))
            article = result.scalars().first()
            if not article:
                return None
            return self._to_dict(article)

    async def update_article(self, article_id: UUID, article_update: ArticleCreate) -> Optional[dict]:
        async with SessionLocal() as session:
            async with session.begin():
                result = await session.execute(select(NewsArticle).filter(NewsArticle.id == article_id))
                article = result.scalars().first()
                if not article:
                    return None
                # Update fields
                article.title = article_update.title
                article.content = normalize_content(article_update.content)
                article.summary = summarize_content(article.content)
                article.author = article_update.author
                article.published_at = article_update.published_at
                article.country = article_update.country
                article.language = article_update.language
                article.entities = json.dumps(extract_entities(article.content))
                article.categories = json.dumps(classify_categories(article.content))
                article.keywords = json.dumps(article_update.keywords)
                relevance, urgency, impact, overall = calculate_scores(article_update, json.loads(article.entities), json.loads(article.categories))
                article.relevance_score = relevance
                article.urgency_score = urgency
                article.impact_score = impact
                article.overall_score = overall
                article.updated_at = None
            await session.commit()
            return self._to_dict(article)

    async def delete_article(self, article_id: UUID) -> bool:
        async with SessionLocal() as session:
            async with session.begin():
                result = await session.execute(delete(NewsArticle).filter(NewsArticle.id == article_id))
                await session.commit()
                return result.rowcount > 0

    async def search_articles(
        self,
        query: Optional[str] = None,
        country: Optional[str] = None,
        language: Optional[str] = None,
        entities: Optional[List[str]] = None,
        categories: Optional[List[str]] = None,
        keywords: Optional[List[str]] = None,
        skip: int = 0,
        limit: int = 50
    ) -> Tuple[List[dict], int]:
        async with SessionLocal() as session:
            filters = []
            if country:
                filters.append(NewsArticle.country == country)
            if language:
                filters.append(NewsArticle.language == language)
            # Filtering entities, categories, keywords is complex, simplified here
            query_stmt = select(NewsArticle)
            for f in filters:
                query_stmt = query_stmt.filter(f)
            result = await session.execute(query_stmt.offset(skip).limit(limit))
            articles = result.scalars().all()
            total = len(articles)  # Simplified count
            article_dicts = [self._to_dict(a) for a in articles]
            return article_dicts, total

    async def rate_article(self, article_id: UUID, user_id: UUID, rating: int, feedback: Optional[str], status: Optional[str]) -> Optional[dict]:
        async with SessionLocal() as session:
            async with session.begin():
                result = await session.execute(select(NewsArticle).filter(NewsArticle.id == article_id))
                article = result.scalars().first()
                if not article:
                    return None
                article.editor_rating = rating
                article.editor_feedback = feedback
                if status:
                    article.status = status
                article.updated_at = None
            await session.commit()
            return self._to_dict(article)

    def _to_dict(self, article: NewsArticle) -> dict:
        return {
            "id": str(article.id),
            "trace_id": str(article.trace_id),
            "source_id": str(article.source_id),
            "source_name": article.source_name,
            "source_type": article.source_type.value if article.source_type else None,
            "url": article.url,
            "title": article.title,
            "content": article.content,
            "summary": article.summary,
            "author": article.author,
            "published_at": article.published_at.isoformat() if article.published_at else None,
            "fetched_at": article.fetched_at.isoformat() if article.fetched_at else None,
            "country": article.country,
            "language": article.language.value if article.language else None,
            "entities": json.loads(article.entities) if article.entities else [],
            "categories": json.loads(article.categories) if article.categories else [],
            "keywords": json.loads(article.keywords) if article.keywords else [],
            "relevance_score": article.relevance_score,
            "urgency_score": article.urgency_score,
            "impact_score": article.impact_score,
            "overall_score": article.overall_score,
            "duplicate_group_id": str(article.duplicate_group_id) if article.duplicate_group_id else None,
            "is_duplicate": article.is_duplicate,
            "duplicate_of_id": str(article.duplicate_of_id) if article.duplicate_of_id else None,
            "status": article.status,
            "editor_rating": article.editor_rating,
            "editor_feedback": article.editor_feedback,
            "approved_by": str(article.approved_by) if article.approved_by else None,
            "approved_at": article.approved_at.isoformat() if article.approved_at else None,
            "prompt_version": article.prompt_version,
            "model_version": article.model_version,
            "created_at": article.created_at.isoformat() if article.created_at else None,
            "updated_at": article.updated_at.isoformat() if article.updated_at else None,
            "deleted_at": article.deleted_at.isoformat() if article.deleted_at else None
        }
