from fastapi import APIRouter, Depends, Query, HTTPException
from typing import Optional, List, Dict, Any
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_

from backend.src.core.database import SessionLocal
from backend.src.core.security import get_current_user, rbac_required

router = APIRouter(prefix="/audit", tags=["Audit"])


@router.get("/logs")
@rbac_required(["admin", "editor"])
async def get_audit_logs(
    user_id: Optional[UUID] = Query(None),
    entity_type: Optional[str] = Query(None),
    entity_id: Optional[UUID] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, gt=0, le=100),
    db: AsyncSession = Depends(SessionLocal),
    current_user_id: UUID = Depends(get_current_user)
) -> List[Dict[str, Any]]:
    conditions = []
    if user_id:
        conditions.append(f"audit_logs.user_id = '{user_id}'")
    if entity_type:
        conditions.append(f"audit_logs.entity_type = '{entity_type}'")
    if entity_id:
        conditions.append(f"audit_logs.entity_id = '{entity_id}'")

    where_clause = " AND ".join(conditions) if conditions else None

    # Use raw SQL query for flexibility
    sql = f"SELECT * FROM audit_logs"
    if where_clause:
        sql += f" WHERE {where_clause}"
    sql += f" ORDER BY created_at DESC OFFSET {skip} LIMIT {limit}"

    result = await db.execute(sql)
    rows = result.fetchall()

    # Convert to list of dict
    entries = []
    for row in rows:
        entries.append(dict(row))
    return entries
