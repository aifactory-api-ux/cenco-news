import httpx
from typing import List, Dict, Any
from datetime import datetime

class ApiCollector:
    async def collect(self, source_config: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Collect articles from a REST API source"""
        url = source_config.get('url')
        headers = source_config.get('headers', {})
        params = source_config.get('params', {})

        if not url:
            raise ValueError("API source config missing 'url'")

        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get(url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()

        articles = []
        items = data.get('items') or data.get('results') or data.get('articles') or []
        for item in items:
            published_str = item.get('published_at') or item.get('published') or item.get('date')
            published = None
            if published_str:
                try:
                    published = datetime.fromisoformat(published_str)
                except ValueError:
                    pass
            article = {
                'url': item.get('url') or item.get('link'),
                'title': item.get('title'),
                'content': item.get('content') or item.get('description', ''),
                'summary': item.get('summary') or item.get('description', ''),
                'author': item.get('author', None),
                'published_at': published
            }
            articles.append(article)

        return articles
