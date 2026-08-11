from uuid import uuid4
from typing import Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from backend.src.models.entities import Base
from sqlalchemy import insert

async def create_audit_log(
    db: AsyncSession,
    event_type: str,
    entity_type: str,
    entity_id: str,
    user_id: Optional[str],
    action: str,
    changes: Optional[Dict[str, Any]] = None,
    old_values: Optional[Dict[str, Any]] = None,
    new_values: Optional[Dict[str, Any]] = None
) -> None:
    audit_log_id = uuid4()

    query = insert(Base.metadata.tables['audit_logs']).values(
        id=audit_log_id,
        event_type=event_type,
        entity_type=entity_type,
        entity_id=entity_id,
        user_id=user_id,
        action=action,
        changes=changes,
        old_values=old_values,
        new_values=new_values
    )

    await db.execute(query)
    # Commit is caller responsibility
