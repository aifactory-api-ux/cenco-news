from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from typing import List, Tuple
from datetime import datetime

from backend.src.models.audit import AuditLog
from backend.src.schemas.audit import AuditLog as SchemaAuditLog, AuditLogFilter

async def list_audit_logs(
    db: AsyncSession,
    filters: AuditLogFilter,
    page: int = 1,
    page_size: int = 20
) -> Tuple[List[SchemaAuditLog], int]:
    query = select(AuditLog)
    conditions = []

    if filters.user_id:
        conditions.append(AuditLog.user_id == filters.user_id)
    if filters.action:
        conditions.append(AuditLog.action == filters.action)
    if filters.resource_type:
        conditions.append(AuditLog.resource_type == filters.resource_type)
    if filters.resource_id:
        conditions.append(AuditLog.resource_id == filters.resource_id)
    if filters.start_date:
        conditions.append(AuditLog.created_at >= filters.start_date)
    if filters.end_date:
        conditions.append(AuditLog.created_at <= filters.end_date)

    if conditions:
        query = query.filter(and_(*conditions))

    total_result = await db.execute(query)
    total = total_result.scalars().count()

    offset = (page - 1) * page_size
    query = query.offset(offset).limit(page_size)

    result = await db.execute(query)
    audit_logs = result.scalars().all()

    return ([SchemaAuditLog.from_orm(log) for log in audit_logs], total)
