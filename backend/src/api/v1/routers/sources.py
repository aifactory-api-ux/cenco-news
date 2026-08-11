from fastapi import APIRouter, Depends, HTTPException, Query, Path, status
from typing import Optional
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from backend.src.schemas import SourceCreate, SourceUpdate
from backend.src.services.source_service import create_source, get_source, list_sources, update_source, update_source_status
from backend.src.core.database import SessionLocal
from backend.src.models.entities import SourceStatus

router = APIRouter(prefix="/sources", tags=["Sources"])


async def get_db() -> AsyncSession:
    async with SessionLocal() as session:
        yield session


@router.get("", status_code=200)
async def list_sources_endpoint(
    status: Optional[SourceStatus] = Query(None),
    is_enabled: Optional[bool] = Query(None),
    country: Optional[str] = Query(None),
    language: Optional[str] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: AsyncSession = Depends(get_db),
):
    result = await list_sources(db, status, is_enabled, country, language, skip, limit)
    return result


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_source_endpoint(
    source_create: SourceCreate,
    db: AsyncSession = Depends(get_db),
):
    source = await create_source(db, source_create)
    return source


@router.get("/{source_id}", status_code=200)
async def get_source_endpoint(
    source_id: UUID = Path(...),
    db: AsyncSession = Depends(get_db),
):
    source = await get_source(db, source_id)
    return source


@router.put("/{source_id}", status_code=200)
async def update_source_endpoint(
    source_id: UUID = Path(...),
    source_update: SourceUpdate = None,
    db: AsyncSession = Depends(get_db),
):
    source = await update_source(db, source_id, source_update)
    return source


@router.patch("/{source_id}/status", status_code=200)
async def update_source_status_endpoint(
    source_id: UUID = Path(...),
    status: SourceStatus = Query(...),
    db: AsyncSession = Depends(get_db),
):
    source = await update_source_status(db, source_id, status)
    return source
