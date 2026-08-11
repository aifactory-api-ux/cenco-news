from typing import Optional, List, Dict, Any
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update
from fastapi import HTTPException
from backend.src.models.entities import Source, SourceStatus
from backend.src.schemas import SourceCreate, SourceUpdate
import json


async def create_source(db: AsyncSession, source_create: SourceCreate) -> Source:
    adapter_config_str = json.dumps(source_create.adapter_config or {})
    new_source = Source(
        name=source_create.name,
        type=source_create.type,
        url=str(source_create.url),
        priority=source_create.priority if source_create.priority else 1,
        country=source_create.country,
        language=source_create.language,
        adapter_config=adapter_config_str,
        is_enabled=source_create.is_enabled if source_create.is_enabled is not None else True,
        status=SourceStatus.ACTIVE
    )
    db.add(new_source)
    await db.commit()
    await db.refresh(new_source)
    return new_source


async def get_source(db: AsyncSession, source_id: UUID) -> Optional[Source]:
    result = await db.execute(select(Source).where(Source.id == source_id))
    source = result.scalars().first()
    if source is None:
        raise HTTPException(status_code=404, detail="Source not found")
    return source


async def list_sources(db: AsyncSession, 
                       status: Optional[SourceStatus] = None,
                       is_enabled: Optional[bool] = None,
                       country: Optional[str] = None,
                       language: Optional[str] = None,
                       skip: int = 0,
                       limit: int = 100) -> Dict[str, Any]:
    query = select(Source)
    if status:
        query = query.where(Source.status == status)
    if is_enabled is not None:
        query = query.where(Source.is_enabled == is_enabled)
    if country:
        query = query.where(Source.country == country)
    if language:
        query = query.where(Source.language == language)
    total = await db.execute(select(Source).count())
    total_count = total.scalar_one()
    result = await db.execute(query.offset(skip).limit(limit))
    items = result.scalars().all()

    return {"items": items, "total": total_count}


async def update_source(db: AsyncSession, source_id: UUID, source_update: SourceUpdate) -> Source:
    source = await get_source(db, source_id)
    for attr, value in source_update.dict(exclude_unset=True).items():
        if attr == "adapter_config" and value is not None:
            setattr(source, attr, json.dumps(value))
        elif value is not None:
            setattr(source, attr, value)
    db.add(source)
    await db.commit()
    await db.refresh(source)
    return source


async def update_source_status(db: AsyncSession, source_id: UUID, status: SourceStatus) -> Source:
    source = await get_source(db, source_id)
    source.status = status
    db.add(source)
    await db.commit()
    await db.refresh(source)
    return source

