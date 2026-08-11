from sqlalchemy.ext.asyncio import AsyncSession
from backend.src.models.user import User
from backend.src.core.security import verify_password
from sqlalchemy.future import select
from fastapi import HTTPException, status


async def authenticate_user(db: AsyncSession, email: str, password: str) -> User | None:
    stmt = select(User).where(User.email == email)
    result = await db.execute(stmt)
    user = result.scalars().first()
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Usuario inactivo")
    return user
