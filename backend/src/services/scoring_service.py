from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from backend.src.models.scoring import ScoringDimension
from backend.src.models.news import NewsItem
from backend.src.schemas.scoring import ScoringDimensionCreate, ScoringDimension as SchemaScoringDimension
from typing import List
from uuid import uuid4
from datetime import datetime

async def list_scoring_dimensions(db: AsyncSession) -> List[SchemaScoringDimension]:
    result = await db.execute(select(ScoringDimension).where(ScoringDimension.is_active == True))
    dimensions = result.scalars().all()
    return [SchemaScoringDimension.from_orm(d) for d in dimensions]

async def create_scoring_dimension(db: AsyncSession, dimension_create: ScoringDimensionCreate) -> SchemaScoringDimension:
    now = datetime.utcnow()
    new_dimension = ScoringDimension(
        id=uuid4(),
        name=dimension_create.name,
        description=dimension_create.description,
        weight=dimension_create.weight,
        is_active=True,
        created_at=now,
        updated_at=now
    )
    db.add(new_dimension)
    await db.commit()
    await db.refresh(new_dimension)
    return SchemaScoringDimension.from_orm(new_dimension)

async def calculate_news_score(db: AsyncSession, news_id) -> float:
    # Fetch active scoring dimensions
    result = await db.execute(select(ScoringDimension).where(ScoringDimension.is_active == True))
    dimensions = result.scalars().all()
    if not dimensions:
        raise ValueError("No active scoring dimensions found")

    # Fetch news item
    result = await db.execute(select(NewsItem).filter(NewsItem.id == news_id))
    news = result.scalar_one_or_none()
    if not news:
        raise ValueError(f"News item with id {news_id} not found")

    # Calculate weighted score based on available dimensions
    total_score = 0.0
    total_weight = 0.0

    # Mapping known dimension names to news scores
    score_map = {
        "relevance": news.relevance_score,
        "urgency": news.urgency_score,
        "impact": news.impact_score,
    }

    for dim in dimensions:
        dim_name_lower = dim.name.lower()
        if dim_name_lower in score_map:
            score_value = score_map[dim_name_lower]
            total_score += dim.weight * score_value
            total_weight += dim.weight

    if total_weight == 0:
        return 0.0

    overall_score = total_score / total_weight

    # Update the news item with the calculated overall score
    news.overall_score = overall_score
    news.updated_at = datetime.utcnow()
    db.add(news)
    await db.commit()

    return overall_score
