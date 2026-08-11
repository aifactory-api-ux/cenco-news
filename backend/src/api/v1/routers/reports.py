from fastapi import APIRouter, Depends, HTTPException, Query, status
from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel
from backend.src.schemas import ReportCreate
from backend.src.services.report_service import ReportService
from backend.src.services.distribution.exporter import Exporter
from backend.src.core.security import get_current_user

router = APIRouter(prefix="/reports", tags=["Reports"])
report_service = ReportService()
exporter = Exporter()

class ReportGenerateRequest(BaseModel):
    country: str
    business_unit: str
    language: str
    date_range_start: str
    date_range_end: str
    include_articles: Optional[List[UUID]] = None
    exclude_articles: Optional[List[UUID]] = None


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_report(report_create: ReportCreate, user_id: UUID = Depends(get_current_user)):
    report = await report_service.create_report(
        title=report_create.title,
        country=report_create.country,
        business_unit=report_create.business_unit,
        language=report_create.language,
        date_range_start=report_create.date_range_start,
        date_range_end=report_create.date_range_end,
        article_ids=report_create.article_ids,
        trace_id=UUID(),
        created_by=user_id
    )
    return report


@router.get("/{report_id}")
async def get_report(report_id: UUID, user_id: UUID = Depends(get_current_user)):
    report = await report_service.get_report(report_id)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    return report


@router.put("/{report_id}")
async def update_report(report_id: UUID, report_update: ReportCreate, user_id: UUID = Depends(get_current_user)):
    update_fields = report_update.dict(exclude_unset=True)
    updated_report = await report_service.update_report(report_id, update_fields)
    if not updated_report:
        raise HTTPException(status_code=404, detail="Report not found")
    return updated_report


@router.delete("/{report_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_report(report_id: UUID, user_id: UUID = Depends(get_current_user)):
    # Actual deletion not implemented for safety; mark as deleted if needed
    # For now, raise 405 to indicate not allowed
    raise HTTPException(status_code=405, detail="Deleting reports is not allowed")


@router.post("/generate")
async def generate_report(request: ReportGenerateRequest, user_id: UUID = Depends(get_current_user)):
    # Create a draft report and generate content (for preview)
    report = await report_service.create_report(
        title=f"Daily Pulse: {request.country} {request.business_unit}",
        country=request.country,
        business_unit=request.business_unit,
        language=request.language,
        date_range_start=request.date_range_start,
        date_range_end=request.date_range_end,
        article_ids=request.include_articles or [],
        trace_id=UUID(),
        created_by=user_id
    )
    # Generate HTML content as default preview
    content = await report_service.generate_report_content(report, "html")
    return {"report_id": report.id, "content": content.decode('utf-8')}


@router.get("/{report_id}/download")
async def download_report(report_id: UUID, format: str = Query("html", regex="^(html|pdf|word)$"), user_id: UUID = Depends(get_current_user)):
    try:
        content = await exporter.export_report(str(report_id), format)
    except ValueError:
        raise HTTPException(status_code=404, detail="Report not found or unsupported format")
    content_type = {
        "html": "text/html",
        "pdf": "application/pdf",
        "word": "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    }[format]
    return {
        "content": content,
        "content_type": content_type
    }
