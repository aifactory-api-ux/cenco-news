from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from uuid import UUID

from backend.src.schemas.prompt import Prompt, PromptCreate
from backend.src.services.prompt_service import (
    list_prompts,
    create_prompt,
    get_prompt_by_id,
    update_prompt,
    delete_prompt
)
from backend.src.api.deps import get_db, get_current_user
from backend.src.models.user import User

router = APIRouter(prefix="/prompts", tags=["prompts"])

@router.get("", response_model=List[Prompt])
async def get_prompts(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    prompts = await list_prompts(db)
    return prompts

@router.post("", response_model=Prompt, status_code=status.HTTP_201_CREATED)
async def post_prompt(
    prompt_create: PromptCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    prompt = await create_prompt(db, prompt_create)
    return prompt

@router.get("/{prompt_id}", response_model=Prompt)
async def get_prompt(
    prompt_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    prompt = await get_prompt_by_id(db, prompt_id)
    if not prompt:
        raise HTTPException(status_code=404, detail="Prompt no encontrado")
    return prompt

@router.put("/{prompt_id}", response_model=Prompt)
async def put_prompt(
    prompt_id: UUID,
    prompt_update: PromptCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    updated = await update_prompt(db, prompt_id, prompt_update)
    if not updated:
        raise HTTPException(status_code=404, detail="Prompt no encontrado para actualizar")
    return updated

@router.delete("/{prompt_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_prompt_route(
    prompt_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    deleted = await delete_prompt(db, prompt_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Prompt no encontrado para eliminar")
