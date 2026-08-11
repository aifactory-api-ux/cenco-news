from celery import shared_task
from sqlalchemy.ext.asyncio import AsyncSession
from backend.src.core.database import SessionLocal
from backend.src.services.source_service import list_sources
from backend.src.services.collectors.collector_factory import CollectorFactory
import asyncio
import json

@shared_task
def collect_news_from_sources():
    """Collect news articles from all active sources."""
    async def run_collection():
        async with SessionLocal() as db:
            # List active and enabled sources
            sources_data = await list_sources(db, status=None, is_enabled=True, skip=0, limit=1000)
            sources = sources_data.get('items', [])

            for source in sources:
                source_type = source.type.value if hasattr(source.type, 'value') else source.type
                adapter_config = json.loads(source.adapter_config) if source.adapter_config else {}

                collector = CollectorFactory.get_collector(source_type)
                try:
                    articles = await collector.collect({**adapter_config, 'url': source.url})
                    # TODO: Store collected articles logic here
                    # e.g. await store_articles(db, source.id, articles)
                    # For now, just print count
                    print(f"Collected {len(articles)} articles from source {source.name}")
                except Exception as e:
                    print(f"Error collecting from source {source.name}: {e}")

    asyncio.run(run_collection())
