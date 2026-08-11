from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Optional
from uuid import UUID
from datetime import datetime
from backend.src.models.news import NewsSource
from backend.src.schemas.source_schemas import NewsSourceCreate, NewsSourceUpdate

class SourceService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all_sources(self) -> List[NewsSource]:
        query = select(NewsSource)
        result = await self.db.execute(query)
        sources = result.scalars().all()
        return sources

    async def create_source(self, source_create: NewsSourceCreate) -> NewsSource:
        now = datetime.utcnow()
        source_data = source_create.dict(exclude_unset=True)
        source = NewsSource(**source_data, created_at=now, updated_at=now)
        self.db.add(source)
        await self.db.commit()
        await self.db.refresh(source)
        return source

    async def get_source_by_id(self, source_id: UUID) -> Optional[NewsSource]:
        query = select(NewsSource).where(NewsSource.id == source_id)
        result = await self.db.execute(query)
        source = result.scalars().first()
        return source

    async def update_source(self, source_id: UUID, source_update: NewsSourceUpdate) -> Optional[NewsSource]:
        source = await self.get_source_by_id(source_id)
        if not source:
            return None
        update_data = source_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(source, key, value)
        source.updated_at = datetime.utcnow()
        await self.db.commit()
        await self.db.refresh(source)
        return source

    async def delete_source(self, source_id: UUID) -> bool:
        source = await self.get_source_by_id(source_id)
        if not source:
            return False
        await self.db.delete(source)
        await self.db.commit()
        return True
