import feedparser
from typing import List, Dict, Any
from datetime import datetime


class RssCollector:
    async def collect(self, source_config: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Collect articles from an RSS or Atom feed URL"""
        url = source_config.get('url')
        if not url:
            raise ValueError("RSS source config missing 'url'")

        feed = feedparser.parse(url)
        articles = []

        for entry in feed.entries:
            published = None
            if hasattr(entry, 'published_parsed') and entry.published_parsed:
                published = datetime(*entry.published_parsed[:6])
            elif hasattr(entry, 'updated_parsed') and entry.updated_parsed:
                published = datetime(*entry.updated_parsed[:6])

            article = {
                'url': entry.link,
                'title': entry.title,
                'content': entry.get('summary', ''),
                'summary': entry.get('summary', ''),
                'author': entry.get('author', None),
                'published_at': published
            }
            articles.append(article)

        return articles
