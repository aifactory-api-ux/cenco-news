from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from backend.src.schemas import UserLogin, TokenResponse
from backend.src.services.auth_service import (
    authenticate_user,
    create_access_token,
    revoke_token,
    refresh_access_token
)
from backend.src.api.deps import get_current_user
from backend.src.services.user_service import get_user_by_id
from typing import Any

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/login", response_model=TokenResponse)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
    access_token = create_access_token(user.id.hex)
    # Optionally update last_login_at
    # User schema may require to convert to dict without password
    return TokenResponse(
        access_token=access_token,
        user=user
    )

@router.post("/logout", status_code=204)
async def logout(current_user: Any = Depends(get_current_user)):
    # Revoke or blacklist token if token management implemented
    revoke_token(current_user)
    return

@router.post("/refresh", response_model=TokenResponse)
async def refresh(token: str):
    new_token, user = await refresh_access_token(token)
    if not new_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired refresh token")
    return TokenResponse(
        access_token=new_token,
        user=user
    )

@router.get("/me", response_model=UserLogin)
async def read_me(current_user_id: str = Depends(get_current_user)):
    user = await get_user_by_id(current_user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user
