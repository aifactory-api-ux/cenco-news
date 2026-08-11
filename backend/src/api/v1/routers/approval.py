from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel, Field
from uuid import UUID

from backend.src.core.database import SessionLocal
from backend.src.services.approval_service import ApprovalService
from backend.src.models.entities import EditorialStatus
from backend.src.schemas import ApprovalCreate
from backend.src.core.security import get_current_user, rbac_required

router = APIRouter(prefix="/approval", tags=["Approval"])


class ApprovalSubmitRequest(BaseModel):
    article_id: UUID
    rating: int = Field(..., ge=1, le=5)
    feedback: str | None = None
    status: EditorialStatus


class BulkApprovalSubmitRequest(BaseModel):
    approvals: List[ApprovalCreate]


@router.post("/submit")
@rbac_required(["editor", "admin"])
async def submit_approval(
    approval: ApprovalSubmitRequest,
    user_id: UUID = Depends(get_current_user),
    db: AsyncSession = Depends(SessionLocal)
):
    article = await ApprovalService.submit_approval(
        db=db,
        article_id=approval.article_id,
        editor_id=user_id,
        rating=approval.rating,
        feedback=approval.feedback,
        status=approval.status,
    )
    return article


@router.post("/bulk")
@rbac_required(["editor", "admin"])
async def submit_bulk_approvals(
    bulk_request: BulkApprovalSubmitRequest,
    user_id: UUID = Depends(get_current_user),
    db: AsyncSession = Depends(SessionLocal)
):
    # Apply approvals, each with the editor_id from current user
    approvals_payload = [
        {
            "article_id": approval.article_id,
            "editor_id": user_id,
            "rating": approval.rating,
            "feedback": approval.feedback,
            "status": approval.status
        }
        for approval in bulk_request.approvals
    ]
    articles = await ApprovalService.bulk_submit_approvals(db=db, approvals=approvals_payload)
    return articles


@router.get("/pending")
@rbac_required(["editor", "admin"])
async def get_pending_approvals(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, gt=0, le=100),
    db: AsyncSession = Depends(SessionLocal),
    user_id: UUID = Depends(get_current_user)
):
    pending_articles = await ApprovalService.list_pending_approvals(db=db, skip=skip, limit=limit)
    return pending_articles
