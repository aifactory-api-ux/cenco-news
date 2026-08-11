from typing import Optional, List
from uuid import UUID
from backend.src.models.entities import User
from backend.src.schemas import UserCreate
from backend.src.core.database import SessionLocal
from sqlalchemy.future import select
from sqlalchemy import update, delete
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from backend.src.core.config import settings
import asyncio

DATABASE_URL_ASYNC = (
    f"postgresql+asyncpg://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}"
)

engine = create_async_engine(DATABASE_URL_ASYNC, future=True, echo=False)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

async def create_user(user_create: UserCreate) -> User:
    async with async_session() as session:
        async with session.begin():
            user = User(
                email=user_create.email,
                name=user_create.name,
                role=user_create.role,
                business_unit=user_create.business_unit,
                country=user_create.country,
                language_preference=user_create.language_preference,
                is_active=True,
                created_at=None,
                updated_at=None
            )
            # Assuming user_create.password is plaintext, hash it here
            from backend.src.core.security import get_password_hash
            user.password_hash = get_password_hash(user_create.password)
            session.add(user)
            await session.commit()
            await session.refresh(user)
            return user

async def get_user_by_email(email: str) -> Optional[User]:
    async with async_session() as session:
        result = await session.execute(select(User).filter_by(email=email))
        user = result.scalars().first()
        return user

async def get_user_by_id(user_id: str) -> Optional[User]:
    async with async_session() as session:
        result = await session.execute(select(User).filter_by(id=user_id))
        user = result.scalars().first()
        return user

async def update_user(user_id: str, user_update: UserCreate) -> Optional[User]:
    async with async_session() as session:
        async with session.begin():
            result = await session.execute(select(User).filter_by(id=user_id))
            user = result.scalars().first()
            if not user:
                return None
            user.email = user_update.email
            user.name = user_update.name
            user.role = user_update.role
            user.business_unit = user_update.business_unit
            user.country = user_update.country
            user.language_preference = user_update.language_preference
            # If password is updated, hash it
            if user_update.password:
                from backend.src.core.security import get_password_hash
                user.password_hash = get_password_hash(user_update.password)
            await session.commit()
            await session.refresh(user)
            return user

async def delete_user(user_id: str) -> bool:
    async with async_session() as session:
        async with session.begin():
            result = await session.execute(delete(User).filter_by(id=user_id))
            if result.rowcount == 0:
                return False
            return True

async def list_users(skip: int = 0, limit: int = 100) -> List[User]:
    async with async_session() as session:
        result = await session.execute(select(User).offset(skip).limit(limit))
        users = result.scalars().all()
        return users
