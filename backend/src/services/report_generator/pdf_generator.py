from weasyprint import HTML
from .html_generator import HTMLReportGenerator

class PDFReportGenerator:
    def __init__(self):
        self.html_generator = HTMLReportGenerator()

    def generate(self, context: dict) -> bytes:
        html_content = self.html_generator.generate(context).decode('utf-8')
        pdf = HTML(string=html_content).write_pdf()
        return pdf
