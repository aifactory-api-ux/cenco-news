from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel
from backend.src.services.deduplication.exact_dedup import ExactDeduplicationService
from backend.src.services.deduplication.semantic_dedup import SemanticDeduplicationService
from backend.src.services.deduplication.embedder import Embedder
from backend.src.core.security import get_current_user

router = APIRouter(prefix="/dedup", tags=["Deduplication"])


class DuplicateCheckRequest(BaseModel):
    article_id: UUID
    content: Optional[str] = None  # for semantic deduplication


class DuplicateArticleResponse(BaseModel):
    id: UUID
    title: str
    similarity_score: Optional[float] = None  # Semantic similarity score
    is_exact: bool = False


@router.get("/articles/{article_id}/duplicates", response_model=List[DuplicateArticleResponse])
async def get_article_duplicates(article_id: UUID, user_id: UUID = Depends(get_current_user)):
    exact_service = ExactDeduplicationService()
    semantic_service = SemanticDeduplicationService()

    # Exact duplicates
    exact_dup = await exact_service.find_exact_duplicate(article_id)
    duplicates = []
    if exact_dup:
        duplicates.append(DuplicateArticleResponse(id=exact_dup.id, title=exact_dup.title, is_exact=True))

    # Semantic duplicates
    embedder = Embedder()
    async with embedder:
        # Fetch article to get content if needed
        semantic_embedding = None
        if exact_dup and exact_dup.content:
            semantic_embedding = await embedder.generate_embedding(exact_dup.content)
        else:
            # Fetch main article content
            semantic_embedding = await embedder.generate_embedding("")

    if semantic_embedding:
        semantic_results = await semantic_service.search_similar_articles(semantic_embedding)
        for article_id_sim, score in semantic_results:
            if not any(d.id == article_id_sim for d in duplicates):
                # Fetch article title
                # TODO: Optimize DB fetch - for now direct DB fetch
                from backend.src.core.database import SessionLocal
                async with SessionLocal() as session:
                    article = await session.get(NewsArticle, article_id_sim)
                    if article:
                        duplicates.append(DuplicateArticleResponse(id=article.id, title=article.title, similarity_score=score))

    return duplicates


@router.post("/check", response_model=List[DuplicateArticleResponse])
async def check_duplicates(request: DuplicateCheckRequest, user_id: UUID = Depends(get_current_user)):
    exact_service = ExactDeduplicationService()
    semantic_service = SemanticDeduplicationService()
    embedder = Embedder()

    duplicates = []

    # Exact match check
    exact_dup = await exact_service.find_exact_duplicate(request.article_id)
    if exact_dup:
        duplicates.append(DuplicateArticleResponse(id=exact_dup.id, title=exact_dup.title, is_exact=True))

    # Semantic similarity check
    if request.content:
        embedding = await embedder.generate_embedding(request.content)
        semantic_results = await semantic_service.search_similar_articles(embedding)
        from backend.src.core.database import SessionLocal
        async with SessionLocal() as session:
            for article_id_sim, score in semantic_results:
                if not any(d.id == article_id_sim for d in duplicates):
                    article = await session.get(NewsArticle, article_id_sim)
                    if article:
                        duplicates.append(DuplicateArticleResponse(id=article.id, title=article.title, similarity_score=score))

    return duplicates
