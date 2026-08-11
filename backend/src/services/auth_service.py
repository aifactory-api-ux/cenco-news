from datetime import datetime, timedelta
from typing import Optional, Tuple
from backend.src.core.security import verify_password, get_password_hash, create_access_token, decode_access_token
from backend.src.models.entities import UserRole
from backend.src.services.user_service import get_user_by_email, get_user_by_id
from backend.src.models.entities import User
from backend.src.core.database import SessionLocal
from sqlalchemy.future import select

async def authenticate_user(email: str, password: str) -> Optional[User]:
    user = await get_user_by_email(email)
    if user and verify_password(password, user.password_hash):
        return user
    return None

async def create_user_with_password(email: str, name: str, role: str, password: str) -> User:
    hashed_password = get_password_hash(password)
    from backend.src.services.user_service import create_user
    return await create_user(email=email, name=name, role=role, password_hash=hashed_password)

# Token management placeholders
revoked_tokens = set()

async def revoke_token(user_id: str):
    # TODO: Implement token revocation strategy (e.g., blacklist tokens stored in Redis)
    revoked_tokens.add(user_id)

async def refresh_access_token(token: str) -> Tuple[Optional[str], Optional[User]]:
    user_id = decode_access_token(token)
    if not user_id:
        return None, None
    user = await get_user_by_id(user_id)
    if not user:
        return None, None
    new_token = create_access_token(user_id)
    return new_token, user
