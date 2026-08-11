from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional
from pydantic import BaseModel
from backend.src.core.security import get_current_user
from backend.src.services.intelligence.scoring import calculate_scores

router = APIRouter(prefix="/scoring", tags=["Scoring"])

class ScoringRule(BaseModel):
    name: str
    weight: float

class ScoringConfig(BaseModel):
    rules: List[ScoringRule]

_scoring_rules_storage = [
    {"name": "relevance", "weight": 1.0},
    {"name": "urgency", "weight": 1.0},
    {"name": "impact", "weight": 1.0}
]

@router.get("/config", response_model=ScoringConfig)
async def get_scoring_config(user_id: str = Depends(get_current_user)):
    return ScoringConfig(rules=[ScoringRule(**rule) for rule in _scoring_rules_storage])

@router.put("/rules")
async def update_scoring_rules(rules: ScoringConfig, user_id: str = Depends(get_current_user)):
    global _scoring_rules_storage
    _scoring_rules_storage = [rule.dict() for rule in rules.rules]
    return {"message": "Scoring rules updated"}
