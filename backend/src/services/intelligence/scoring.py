from typing import List, Tuple
from backend.src.schemas import ArticleCreate

# Scoring logic with weights and ranges

def calculate_scores(article: ArticleCreate, entities: List[str], categories: List[str]) -> Tuple[float, float, float, float]:
    relevance_score = min(len(entities) * 5.0, 33.0)
    urgency_score = 10.0 if 'breaking' in article.title.lower() else 5.0
    impact_score = 20.0 if 'economy' in [c.lower() for c in categories] else 10.0
    overall_score = min(relevance_score + urgency_score + impact_score, 100.0)
    return relevance_score, urgency_score, impact_score, overall_score
