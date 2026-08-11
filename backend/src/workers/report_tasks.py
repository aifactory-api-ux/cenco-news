from celery import Celery
from backend.src.services.report_service import ReportService
from uuid import UUID
from datetime import datetime

app = Celery('report_tasks', broker='pyamqp://guest@localhost//')  # Replace with actual RabbitMQ URL

report_service = ReportService()

@app.task(name='generate_daily_pulse_report')
async def generate_daily_pulse_report(report_id: str, user_id: str):
    report = await report_service.get_report(UUID(report_id))
    if not report:
        raise ValueError(f"Report {report_id} not found")
    # Add logic to generate report content, update status, etc.
    # For demonstration, update generated_at timestamp
    await report_service.update_report(UUID(report_id), {"generated_at": datetime.utcnow()})
    # Return some result indication
    return True
