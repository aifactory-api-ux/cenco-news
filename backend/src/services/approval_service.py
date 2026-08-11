from datetime import datetime
from typing import List, Optional
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException

from backend.src.models.entities import NewsArticle, EditorialStatus
from backend.src.services.audit_service import create_audit_log


class ApprovalService:
    @staticmethod
    async def submit_approval(
        db: AsyncSession,
        article_id: UUID,
        editor_id: UUID,
        rating: int,
        feedback: Optional[str],
        status: EditorialStatus
    ) -> NewsArticle:
        # Validate rating
        if rating < 1 or rating > 5:
            raise HTTPException(status_code=400, detail="Rating must be between 1 and 5")

        # Validate status
        if status not in [EditorialStatus.APPROVED, EditorialStatus.REJECTED]:
            raise HTTPException(status_code=400, detail="Invalid status for approval submission")

        # Load the article
        result = await db.execute(select(NewsArticle).filter(NewsArticle.id == article_id))
        article = result.scalars().first()
        if not article:
            raise HTTPException(status_code=404, detail="News article not found")

        # Only allow approval if article is pending
        if article.status != EditorialStatus.PENDING:
            raise HTTPException(status_code=400, detail="Only pending articles can be approved or rejected")

        # Update article with approval info
        article.editor_rating = rating
        article.editor_feedback = feedback
        article.status = status
        article.approved_by = editor_id if status == EditorialStatus.APPROVED else None
        article.approved_at = datetime.utcnow() if status == EditorialStatus.APPROVED else None

        db.add(article)

        # Create audit log for approval
        await create_audit_log(
            db=db,
            event_type='approval',
            entity_type='news_article',
            entity_id=article_id,
            user_id=editor_id,
            action=f"Article {status.value} with rating {rating}",
            changes={
                "editor_rating": rating,
                "editor_feedback": feedback,
                "status": status.value
            },
            old_values=None,
            new_values={
                "editor_rating": rating,
                "editor_feedback": feedback,
                "status": status.value
            }
        )

        await db.commit()
        await db.refresh(article)

        return article

    @staticmethod
    async def bulk_submit_approvals(db: AsyncSession, approvals: List[dict]) -> List[NewsArticle]:
        articles_updated = []
        for approval in approvals:
            article = await ApprovalService.submit_approval(
                db=db,
                article_id=approval['article_id'],
                editor_id=approval['editor_id'],
                rating=approval['rating'],
                feedback=approval.get('feedback'),
                status=EditorialStatus(approval['status'])
            )
            articles_updated.append(article)
        return articles_updated

    @staticmethod
    async def list_pending_approvals(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[NewsArticle]:
        result = await db.execute(
            select(NewsArticle)
            .filter(NewsArticle.status == EditorialStatus.PENDING)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()
