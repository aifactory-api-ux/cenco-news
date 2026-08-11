import httpx
from bs4 import BeautifulSoup
from typing import List, Dict, Any
from datetime import datetime

class WebCollector:
    async def collect(self, source_config: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Collect articles by web scraping"""
        url = source_config.get('url')
        if not url:
            raise ValueError("Web source config missing 'url'")

        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get(url)
            response.raise_for_status()
            html = response.text

        soup = BeautifulSoup(html, 'html.parser')

        articles = []

        # A very basic scraper example, can be customized with CSS selectors from adapter_config
        article_tags = soup.select('article') or []

        for article_tag in article_tags:
            title_tag = article_tag.select_one('h1, h2, h3')
            title = title_tag.get_text(strip=True) if title_tag else 'No Title'
            content_tag = article_tag.select_one('p')
            content = content_tag.get_text(strip=True) if content_tag else ''

            published = None
            time_tag = article_tag.select_one('time')
            if time_tag and time_tag.has_attr('datetime'):
                try:
                    published = datetime.fromisoformat(time_tag['datetime'])
                except Exception:
                    pass

            article = {
                'url': url,
                'title': title,
                'content': content,
                'summary': content[:200],  # excerpt
                'author': None,
                'published_at': published
            }
            articles.append(article)

        return articles
