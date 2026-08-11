from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional
from pydantic import BaseModel
from uuid import UUID
from backend.src.core.security import get_current_user

router = APIRouter(prefix="/prompts", tags=["Prompts"])

# This is a placeholder: Implement prompt CRUD with in-memory store for demo
_PROMPTS_STORE = {}

class PromptCreate(BaseModel):
    name: str
    content: str

class PromptUpdate(BaseModel):
    name: Optional[str]
    content: Optional[str]

class PromptResponse(BaseModel):
    id: UUID
    name: str
    content: str


@router.get("/", response_model=List[PromptResponse])
async def list_prompts(user_id: UUID = Depends(get_current_user)):
    return [prompt for prompt in _PROMPTS_STORE.values()]


@router.post("/", response_model=PromptResponse)
async def create_prompt(prompt: PromptCreate, user_id: UUID = Depends(get_current_user)):
    import uuid
    new_id = uuid.uuid4()
    new_prompt = PromptResponse(id=new_id, name=prompt.name, content=prompt.content)
    _PROMPTS_STORE[str(new_id)] = new_prompt
    return new_prompt


@router.put("/{prompt_id}")
async def update_prompt(prompt_id: UUID, prompt_update: PromptUpdate, user_id: UUID = Depends(get_current_user)):
    existing = _PROMPTS_STORE.get(str(prompt_id))
    if not existing:
        raise HTTPException(status_code=404, detail="Prompt not found")
    if prompt_update.name is not None:
        existing.name = prompt_update.name
    if prompt_update.content is not None:
        existing.content = prompt_update.content
    _PROMPTS_STORE[str(prompt_id)] = existing
    return existing


@router.delete("/{prompt_id}", status_code=204)
async def delete_prompt(prompt_id: UUID, user_id: UUID = Depends(get_current_user)):
    if str(prompt_id) in _PROMPTS_STORE:
        del _PROMPTS_STORE[str(prompt_id)]
