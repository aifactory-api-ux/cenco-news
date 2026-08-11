from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from uuid import UUID
from datetime import datetime

from backend.src.schemas.audit import AuditLog, AuditLogFilter, AuditLogListResponse
from backend.src.services.audit_service import list_audit_logs
from backend.src.api.deps import get_db, get_current_user
from backend.src.models.user import User

router = APIRouter(prefix="/audit", tags=["audit"])

@router.get("", response_model=AuditLogListResponse)
async def get_audit_logs(
    user_id: Optional[UUID] = None,
    action: Optional[str] = None,
    resource_type: Optional[str] = None,
    resource_id: Optional[UUID] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    page: int = 1,
    page_size: int = 20,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    filters = AuditLogFilter(
        user_id=user_id,
        action=action,
        resource_type=resource_type,
        resource_id=resource_id,
        start_date=start_date,
        end_date=end_date
    )
    audit_logs, total = await list_audit_logs(db, filters, page, page_size)
    pages = (total // page_size) + (1 if total % page_size > 0 else 0)
    return AuditLogListResponse(
        items=audit_logs,
        total=total,
        page=page,
        page_size=page_size,
        pages=pages
    )
