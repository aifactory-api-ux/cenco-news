from celery import Celery
from backend.src.services.article_service import ArticleService
from backend.src.core.config import settings

celery_app = Celery('intelligence_tasks')
celery_app.conf.broker_url = f"amqp://{settings.RABBITMQ_USER}:{settings.RABBITMQ_PASSWORD}@{settings.RABBITMQ_HOST}:{settings.RABBITMQ_PORT}//"

@celery_app.task
def process_article(article_id: str):
    service = ArticleService()
    # Async context not possible here, wrap as sync function
    import asyncio
    asyncio.run(service.process_article(article_id))
