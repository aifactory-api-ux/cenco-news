from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from uuid import UUID

from backend.src.schemas.report import (
    ReportCreate, Report, ReportTemplate, ReportWithNews
)
from backend.src.services.report_service import (
    list_reports,
    create_report,
    get_report_by_id,
    update_report,
    delete_report,
    approve_report,
    send_report,
    list_report_templates
)
from backend.src.api.deps import get_db, get_current_user
from backend.src.models.user import User

router = APIRouter(prefix="/reports", tags=["reports"])

@router.get("", response_model=List[Report])
async def get_reports(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    reports = await list_reports(db)
    return reports

@router.post("", response_model=Report, status_code=status.HTTP_201_CREATED)
async def post_report(
    report_create: ReportCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    report = await create_report(db, report_create, current_user)
    return report

@router.get("/{report_id}", response_model=ReportWithNews)
async def get_report(
    report_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    report = await get_report_by_id(db, report_id)
    if not report:
        raise HTTPException(status_code=404, detail="Reporte no encontrado")
    return report

@router.put("/{report_id}", response_model=Report)
async def put_report(
    report_id: UUID,
    report_update: ReportCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    updated_report = await update_report(db, report_id, report_update)
    if not updated_report:
        raise HTTPException(status_code=404, detail="Reporte no encontrado para actualizar")
    return updated_report

@router.delete("/{report_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_report_route(
    report_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    deleted = await delete_report(db, report_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Reporte no encontrado para eliminar")

@router.post("/{report_id}/approve", status_code=status.HTTP_200_OK)
async def approve_report_route(
    report_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    success = await approve_report(db, report_id, current_user)
    if not success:
        raise HTTPException(status_code=404, detail="Reporte no encontrado o ya aprobado")
    return {"message": "Reporte aprobado correctamente"}

@router.post("/{report_id}/send", status_code=status.HTTP_200_OK)
async def send_report_route(
    report_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    sent = await send_report(db, report_id)
    if not sent:
        raise HTTPException(status_code=404, detail="Reporte no encontrado o error al enviar")
    return {"message": "Reporte enviado correctamente"}

@router.get("/templates", response_model=List[ReportTemplate])
async def get_report_templates(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    templates = await list_report_templates(db)
    return templates
