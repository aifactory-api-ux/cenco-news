from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials
from fastapi.security import HTTPBearer
from backend.src.core.security import decode_access_token
from backend.src.services.user_service import get_user_by_id

security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    token = credentials.credentials
    user_id = decode_access_token(token)
    if user_id is None:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    user = await get_user_by_id(user_id)
    if not user or not user.is_active:
        raise HTTPException(status_code=403, detail="User inactive or not found")
    return user.id.hex

async def require_role(roles: list):
    async def role_checker(current_user_id: str = Depends(get_current_user)):
        user = await get_user_by_id(current_user_id)
        if user.role not in roles:
            raise HTTPException(status_code=403, detail="Forbidden")
        return current_user_id
    return role_checker
