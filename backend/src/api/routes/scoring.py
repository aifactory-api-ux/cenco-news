from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from uuid import UUID

from backend.src.schemas.scoring import ScoringDimensionCreate, ScoringDimension
from backend.src.services.scoring_service import (
    list_scoring_dimensions,
    create_scoring_dimension,
    calculate_news_score,
)
from backend.src.api.deps import get_db, get_current_user
from backend.src.models.user import User

router = APIRouter(prefix="/scoring", tags=["scoring"])

@router.get("/dimensions", response_model=List[ScoringDimension])
async def get_scoring_dimensions(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    dimensions = await list_scoring_dimensions(db)
    return dimensions

@router.post("/dimensions", response_model=ScoringDimension, status_code=status.HTTP_201_CREATED)
async def post_scoring_dimension(
    dimension_create: ScoringDimensionCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    dimension = await create_scoring_dimension(db, dimension_create)
    return dimension

@router.post("/calculate/{news_id}")
async def post_calculate_score(
    news_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        score = await calculate_news_score(db, news_id)
        return {"news_id": str(news_id), "score": score}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
