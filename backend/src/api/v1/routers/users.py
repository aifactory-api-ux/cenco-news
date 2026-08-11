from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from uuid import UUID
from backend.src.schemas import UserCreate
from backend.src.services.user_service import (
    create_user,
    get_user_by_id,
    update_user,
    delete_user,
    list_users
)
from backend.src.api.deps import get_current_user, require_role
from backend.src.models.entities import UserRole
from backend.src.schemas import UserCreate

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", status_code=201)
async def api_create_user(user_create: UserCreate, current_user_id: UUID = Depends(get_current_user)):
    await require_role(["admin"])(lambda user_id=current_user_id: None)()  # check admin role
    return await create_user(user_create)

@router.get("/me")
async def api_get_me(current_user_id: UUID = Depends(get_current_user)):
    user = await get_user_by_id(current_user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/{user_id}")
async def api_get_user(user_id: UUID, current_user_id: UUID = Depends(get_current_user)):
    await require_role(["admin", "editor"])(lambda user_id=current_user_id: None)()  # check admin or editor role
    user = await get_user_by_id(user_id.hex)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/{user_id}")
async def api_update_user(user_id: UUID, user_update: UserCreate, current_user_id: UUID = Depends(get_current_user)):
    await require_role(["admin"])(lambda user_id=current_user_id: None)()  # check admin role
    user = await update_user(user_id.hex, user_update)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.delete("/{user_id}", status_code=204)
async def api_delete_user(user_id: UUID, current_user_id: UUID = Depends(get_current_user)):
    await require_role(["admin"])(lambda user_id=current_user_id: None)()  # check admin role
    success = await delete_user(user_id.hex)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return

@router.get("/")
async def api_list_users(skip: int = 0, limit: int = 100, current_user_id: UUID = Depends(get_current_user)):
    await require_role(["admin"])(lambda user_id=current_user_id: None)()  # check admin role
    return await list_users(skip, limit)
