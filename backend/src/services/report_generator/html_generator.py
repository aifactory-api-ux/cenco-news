from jinja2 import Environment, PackageLoader, select_autoescape

class HTMLReportGenerator:
    def __init__(self):
        self.env = Environment(
            loader=PackageLoader('backend.src.services.report_generator', 'templates'),
            autoescape=select_autoescape(['html', 'xml'])
        )

    def generate(self, context: dict) -> bytes:
        template = self.env.get_template('report_template.html')
        html_content = template.render(**context)
        return html_content.encode('utf-8')
