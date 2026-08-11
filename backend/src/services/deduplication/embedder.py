from typing import List
import os
from dotenv import load_dotenv
import httpx

load_dotenv()

# This embedder service will assume an external vector embedding service is available
# We default to OpenAI embeddings but must be configurable to support open source or local models

class Embedder:
    def __init__(self):
        self.api_url = os.getenv('EMBEDDING_API_URL')
        self.api_key = os.getenv('EMBEDDING_API_KEY')

        if not self.api_url or not self.api_key:
            raise ValueError('Embedding API URL and API Key must be set in environment variables')

        self.headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }

    async def generate_embedding(self, text: str) -> List[float]:
        # Make an HTTP request to the embedding API
        async with httpx.AsyncClient() as client:
            body = {"input": text}
            response = await client.post(self.api_url, json=body, headers=self.headers, timeout=10.0)
            response.raise_for_status()
            json_resp = response.json()
            # Expected response: {"embedding": [float,...]}
            embedding = json_resp.get('embedding')
            if not embedding:
                raise RuntimeError('Embedding not returned by API')
            return embedding

    async def generate_embeddings_bulk(self, texts: List[str]) -> List[List[float]]:
        embeddings = []
        for text in texts:
            emb = await self.generate_embedding(text)
            embeddings.append(emb)
        return embeddings
