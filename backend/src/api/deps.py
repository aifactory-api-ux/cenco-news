from typing import Optional
from fastapi import Depends, HTTPException, Query
from fastapi.security import OAuth2PasswordRequestForm
from backend.src.core.security import get_current_user, require_roles
from backend.src.db.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession


async def get_db_session() -> AsyncSession:
    async for session in get_db():
        yield session


async def current_user(user=Depends(get_current_user)):
    return user


def require_roles_dependency(*roles: str):
    return require_roles(*roles)


def get_pagination(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100)
):
    return page, page_size
