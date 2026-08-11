from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from backend.src.services.user_service import authenticate_user
from backend.src.core.security import create_access_token
from backend.src.db.database import get_db
from pydantic import BaseModel
from datetime import timedelta

router = APIRouter()


class LoginRequest(BaseModel):
    email: str
    password: str


class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    expires_in: int


class RefreshRequest(BaseModel):
    refresh_token: str


class RefreshResponse(BaseModel):
    access_token: str
    expires_in: int


@router.post("/auth/login", response_model=LoginResponse)
async def login(request: LoginRequest, db: AsyncSession = Depends(get_db)):
    user = await authenticate_user(db, request.email, request.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Correo o contraseña incorrectos")

    access_token_expires = timedelta(minutes=60 * 24)  # 1 day
    access_token = create_access_token(
        data={"sub": user.email, "role": user.role.value}, expires_delta=access_token_expires
    )

    # For simplicity, refresh token is same as access token in this implementation
    refresh_token = access_token

    return LoginResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        expires_in=access_token_expires.total_seconds(),
    )


@router.post("/auth/refresh", response_model=RefreshResponse)
async def refresh_token(request: RefreshRequest):
    # For simplicity, token refresh logic is minimal
    try:
        payload = create_access_token(data={}, expires_delta=None)  # Invalidate old token logic not implemented here
        token = create_access_token(data=payload)
        expires_in = 60 * 24 * 60
        return RefreshResponse(access_token=token, expires_in=expires_in)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido o expirado")
