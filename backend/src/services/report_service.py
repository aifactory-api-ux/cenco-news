import json
from typing import List, Optional, Dict, Any
from datetime import datetime, date
from uuid import UUID, uuid4
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update
from backend.src.models.entities import Report, ReportStatus
from backend.src.core.database import SessionLocal
from backend.src.services.report_generator.html_generator import HTMLReportGenerator
from backend.src.services.report_generator.pdf_generator import PDFReportGenerator
from backend.src.services.report_generator.docx_generator import DOCXReportGenerator

class ReportService:
    def __init__(self):
        self.html_generator = HTMLReportGenerator()
        self.pdf_generator = PDFReportGenerator()
        self.docx_generator = DOCXReportGenerator()

    async def create_report(self, title: str, country: str, business_unit: str, language: str,
                            date_range_start: date, date_range_end: date, article_ids: List[UUID], 
                            trace_id: UUID, created_by: UUID) -> Report:
        async with SessionLocal() as session:
            report = Report(
                id=uuid4(),
                title=title,
                country=country,
                business_unit=business_unit,
                language=language,
                status=ReportStatus.DRAFT,
                date_range_start=date_range_start,
                date_range_end=date_range_end,
                articles=article_ids,
                summary=None,
                generated_at=datetime.utcnow(),
                published_at=None,
                distributed_at=None,
                prompt_version="v1",
                model_version="v1",
                trace_id=trace_id,
                created_by=created_by,
                approved_by=None,
                approved_at=None,
                revision_history=[],
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            session.add(report)
            await session.commit()
            return report

    async def get_report(self, report_id: UUID) -> Optional[Report]:
        async with SessionLocal() as session:
            result = await session.execute(select(Report).filter(Report.id == report_id))
            return result.scalar_one_or_none()

    async def update_report(self, report_id: UUID, update_fields: Dict[str, Any]) -> Optional[Report]:
        async with SessionLocal() as session:
            await session.execute(update(Report).filter(Report.id == report_id).values(**update_fields))
            await session.commit()
            return await self.get_report(report_id)

    async def generate_report_content(self, report: Report, export_format: str) -> bytes:
        # Fetch articles and build context here if needed
        # For simplicity, here we assume report.articles exist and are IDs
        # Normally would fetch article data and integrate with templates

        # For demonstration, create dummy context
        context = {
            "title": report.title,
            "summary": report.summary or "",
            "date_range_start": report.date_range_start,
            "date_range_end": report.date_range_end,
            "articles": report.articles,
            "business_unit": report.business_unit,
            "country": report.country,
            "language": report.language
        }

        if export_format == "html":
            return self.html_generator.generate(context)
        elif export_format == "pdf":
            return self.pdf_generator.generate(context)
        elif export_format == "word":
            return self.docx_generator.generate(context)
        else:
            raise ValueError(f"Unsupported export format: {export_format}")

