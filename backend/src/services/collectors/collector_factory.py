from typing import Any, Dict
from backend.src.services.collectors.rss_collector import RssCollector
from backend.src.services.collectors.api_collector import ApiCollector
from backend.src.services.collectors.web_collector import WebCollector
from backend.src.services.collectors.pdf_collector import PdfCollector
from backend.src.services.collectors.audio_collector import AudioCollector


class CollectorFactory:
    @staticmethod
    def get_collector(source_type: str) -> Any:
        if source_type == 'rss':
            return RssCollector()
        elif source_type == 'api':
            return ApiCollector()
        elif source_type == 'scraper':
            return WebCollector()
        elif source_type == 'pdf':
            return PdfCollector()
        elif source_type == 'audio':
            return AudioCollector()
        else:
            raise ValueError(f"Unsupported source type: {source_type}")
