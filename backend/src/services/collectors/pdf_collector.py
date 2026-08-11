import fitz  # PyMuPDF
from typing import List, Dict, Any
import io
import httpx
from datetime import datetime

class PdfCollector:
    async def collect(self, source_config: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Collect articles by extracting text from PDF"""
        url = source_config.get('url')
        if not url:
            raise ValueError("PDF source config missing 'url'")

        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get(url)
            response.raise_for_status()
            pdf_bytes = response.content

        pdf_document = fitz.open(stream=pdf_bytes, filetype="pdf")
        full_text = []
        for page_num in range(pdf_document.page_count):
            page = pdf_document.load_page(page_num)
            full_text.append(page.get_text())

        content = '\n'.join(full_text)

        # Basic dummy article from PDF content
        article = {
            'url': url,
            'title': source_config.get('title', 'PDF Document'),
            'content': content,
            'summary': content[:500],
            'author': source_config.get('author', None),
            'published_at': source_config.get('published_at', datetime.utcnow())
        }

        return [article]
