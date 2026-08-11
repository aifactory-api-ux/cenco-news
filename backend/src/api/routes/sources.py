from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from backend.src.api.deps import current_user, require_roles_dependency, get_db_session
from backend.src.schemas.source_schemas import NewsSourceCreate, NewsSourceUpdate, NewsSource
from backend.src.services.source_service import SourceService

router = APIRouter()


@router.get("/sources", response_model=List[NewsSource])
async def list_sources(
    db: AsyncSession = Depends(get_db_session),
    user=Depends(current_user),
):
    source_service = SourceService(db)
    sources = await source_service.get_all_sources()
    return sources


@router.post("/sources", response_model=NewsSource)
async def create_source(
    source_create: NewsSourceCreate,
    db: AsyncSession = Depends(get_db_session),
    user=Depends(require_roles_dependency("admin", "manager")),
):
    source_service = SourceService(db)
    source = await source_service.create_source(source_create)
    return source


@router.get("/sources/{source_id}", response_model=NewsSource)
async def get_source(
    source_id: UUID,
    db: AsyncSession = Depends(get_db_session),
    user=Depends(current_user),
):
    source_service = SourceService(db)
    source = await source_service.get_source_by_id(source_id)
    if not source:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Fuente no encontrada")
    return source


@router.put("/sources/{source_id}", response_model=NewsSource)
async def update_source(
    source_id: UUID,
    source_update: NewsSourceUpdate,
    db: AsyncSession = Depends(get_db_session),
    user=Depends(require_roles_dependency("admin", "manager")),
):
    source_service = SourceService(db)
    updated_source = await source_service.update_source(source_id, source_update)
    if not updated_source:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Fuente no encontrada")
    return updated_source


@router.delete("/sources/{source_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_source(
    source_id: UUID,
    db: AsyncSession = Depends(get_db_session),
    user=Depends(require_roles_dependency("admin")),
):
    source_service = SourceService(db)
    deleted = await source_service.delete_source(source_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Fuente no encontrada")
    return None
