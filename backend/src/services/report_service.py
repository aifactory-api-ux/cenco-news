from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from sqlalchemy.orm import selectinload
from typing import List, Optional
from uuid import UUID, uuid4
from datetime import datetime
import json

from backend.src.models.report import Report, ReportTemplate, ReportStatus
from backend.src.models.news import NewsItem
from backend.src.schemas.report import ReportCreate, Report, ReportWithNews, ReportTemplate as SchemaReportTemplate
from jinja2 import Template
from weasyprint import HTML
from io import BytesIO

async def list_reports(db: AsyncSession) -> List[Report]:
    result = await db.execute(select(Report))
    reports = result.scalars().all()
    return [Report.from_orm(r) for r in reports]

async def create_report(db: AsyncSession, report_create: ReportCreate, user) -> Report:
    now = datetime.utcnow()
    new_report = Report(
        id=uuid4(),
        title=report_create.title,
        template_id=report_create.template_id,
        country_filter=report_create.country_filter,
        language_filter=report_create.language_filter,
        date_from=report_create.date_from,
        date_to=report_create.date_to,
        min_score=report_create.min_score,
        status=ReportStatus.DRAFT,
        content_html=None,
        created_by=user.id,
        created_at=now,
        updated_at=now
    )
    db.add(new_report)
    await db.commit()
    await db.refresh(new_report)

    # Generate Report content HTML
    await generate_report_content(db, new_report.id)

    return Report.from_orm(new_report)

async def get_report_by_id(db: AsyncSession, report_id: UUID) -> Optional[ReportWithNews]:
    result = await db.execute(
        select(Report).options(selectinload(Report.template)).filter(Report.id == report_id)
    )
    report = result.scalars().first()
    if not report:
        return None

    # Fetch news items filtered by report criteria
    news_query = select(NewsItem)

    if report.country_filter:
        news_query = news_query.filter(NewsItem.country == report.country_filter)
    if report.language_filter:
        news_query = news_query.filter(NewsItem.language == report.language_filter)
    if report.date_from:
        news_query = news_query.filter(NewsItem.published_at >= report.date_from)
    if report.date_to:
        news_query = news_query.filter(NewsItem.published_at <= report.date_to)
    if report.min_score is not None:
        news_query = news_query.filter(NewsItem.overall_score >= report.min_score)

    news_result = await db.execute(news_query)
    news_items = news_result.scalars().all()

    report_with_news = ReportWithNews.from_orm(report)
    report_with_news.news_items = news_items
    return report_with_news

async def update_report(db: AsyncSession, report_id: UUID, report_update: ReportCreate) -> Optional[Report]:
    result = await db.execute(select(Report).filter(Report.id == report_id))
    report = result.scalar_one_or_none()
    if not report:
        return None

    for field, value in report_update.dict(exclude_unset=True).items():
        setattr(report, field, value)
    report.updated_at = datetime.utcnow()
    db.add(report)
    await db.commit()
    await db.refresh(report)

    # Regenerate report content if relevant fields changed
    await generate_report_content(db, report_id)

    return Report.from_orm(report)

async def delete_report(db: AsyncSession, report_id: UUID) -> bool:
    result = await db.execute(select(Report).filter(Report.id == report_id))
    report = result.scalar_one_or_none()
    if not report:
        return False
    await db.delete(report)
    await db.commit()
    return True

async def approve_report(db: AsyncSession, report_id: UUID, user) -> bool:
    result = await db.execute(select(Report).filter(Report.id == report_id))
    report = result.scalar_one_or_none()
    if not report or report.status == ReportStatus.APPROVED:
        return False
    report.status = ReportStatus.APPROVED
    report.approved_by = user.id
    report.approved_at = datetime.utcnow()
    report.updated_at = datetime.utcnow()
    db.add(report)
    await db.commit()
    return True

async def send_report(db: AsyncSession, report_id: UUID) -> bool:
    result = await db.execute(select(Report).filter(Report.id == report_id))
    report = result.scalar_one_or_none()
    if not report:
        return False
    # Sending logic placeholder - e.g. email, notifications
    report.status = ReportStatus.SENT
    report.published_at = datetime.utcnow()
    report.updated_at = datetime.utcnow()
    db.add(report)
    await db.commit()
    return True

async def list_report_templates(db: AsyncSession) -> List[SchemaReportTemplate]:
    result = await db.execute(select(ReportTemplate).filter(ReportTemplate.is_active == True))
    templates = result.scalars().all()
    return [SchemaReportTemplate.from_orm(t) for t in templates]

async def generate_report_content(db: AsyncSession, report_id: UUID) -> None:
    result = await db.execute(select(Report).filter(Report.id == report_id))
    report = result.scalar_one_or_none()
    if not report:
        return

    template_content = "<h1>Reporte sin plantilla activa</h1>"
    if report.template_id:
        temp_result = await db.execute(select(ReportTemplate).filter(ReportTemplate.id == report.template_id))
        template = temp_result.scalar_one_or_none()
        if template:
            template_content = template.template_content

    # Fetch news items with filters
    news_query = select(NewsItem)
    if report.country_filter:
        news_query = news_query.filter(NewsItem.country == report.country_filter)
    if report.language_filter:
        news_query = news_query.filter(NewsItem.language == report.language_filter)
    if report.date_from:
        news_query = news_query.filter(NewsItem.published_at >= report.date_from)
    if report.date_to:
        news_query = news_query.filter(NewsItem.published_at <= report.date_to)
    if report.min_score is not None:
        news_query = news_query.filter(NewsItem.overall_score >= report.min_score)

    news_result = await db.execute(news_query)
    news_items = news_result.scalars().all()

    # Render template with Jinja2
    template = Template(template_content)
    rendered_html = template.render(report=report, news_items=news_items)

    # Generate PDF
    pdf_bytes = HTML(string=rendered_html).write_pdf()

    # Save content as HTML in DB
    report.content_html = rendered_html
    report.updated_at = datetime.utcnow()
    db.add(report)
    await db.commit()

    # Optional: Save PDF elsewhere, e.g., storage service
    # Example skipped for brevity
