from typing import List, Optional, Tuple
from uuid import UUID
from backend.src.core.database import SessionLocal
from backend.src.models.entities import NewsArticle
import httpx
import os

class SemanticDeduplicationService:
    """Service for semantic duplicate detection using vector embeddings and Qdrant."""

    def __init__(self):
        self.qdrant_url = os.getenv('QDRANT_URL')
        self.qdrant_api_key = os.getenv('QDRANT_API_KEY')

        if not self.qdrant_url:
            raise RuntimeError('Qdrant URL must be set in environment variables')

        self.headers = {}
        if self.qdrant_api_key:
            self.headers['Authorization'] = f'Bearer {self.qdrant_api_key}'

    async def insert_embedding(self, article_id: UUID, embedding: List[float]):
        async with httpx.AsyncClient() as client:
            data = {
                "points": [
                    {
                        "id": str(article_id),
                        "vector": embedding,
                        "payload": {}
                    }
                ]
            }
            url = f"{self.qdrant_url}/collections/news_articles/points"
            r = await client.put(url, json=data, headers=self.headers, timeout=10.0)
            r.raise_for_status()

    async def search_similar_articles(self, embedding: List[float], limit: int = 5, threshold: float = 0.8) -> List[Tuple[UUID, float]]:
        async with httpx.AsyncClient() as client:
            query = {
                "vector": embedding,
                "limit": limit,
                "with_payload": False,
                "score_threshold": threshold
            }
            url = f"{self.qdrant_url}/collections/news_articles/points/search"
            r = await client.post(url, json=query, headers=self.headers, timeout=10.0)
            r.raise_for_status()
            results = r.json().get('result', [])
            # Return list of tuples (article_id, score)
            return [(UUID(item['id']), item['score']) for item in results]
