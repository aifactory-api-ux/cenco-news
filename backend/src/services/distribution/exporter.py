from typing import Literal
from backend.src.services.report_service import ReportService

class Exporter:
    def __init__(self):
        self.report_service = ReportService()

    async def export_report(self, report_id: str, export_format: Literal['html', 'pdf', 'word']) -> bytes:
        # Fetch report by id and generate content
        report = await self.report_service.get_report(report_id)
        if not report:
            raise ValueError('Report not found')
        content_bytes = await self.report_service.generate_report_content(report, export_format)
        return content_bytes
