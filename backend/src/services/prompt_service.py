from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from uuid import uuid4
from datetime import datetime

from backend.src.models.prompt import Prompt
from backend.src.schemas.prompt import PromptCreate, Prompt as SchemaPrompt

async def list_prompts(db: AsyncSession) -> List[SchemaPrompt]:
    result = await db.execute(select(Prompt).filter(Prompt.is_active == True))
    prompts = result.scalars().all()
    return [SchemaPrompt.from_orm(p) for p in prompts]

async def create_prompt(db: AsyncSession, prompt_create: PromptCreate) -> SchemaPrompt:
    now = datetime.utcnow()
    new_prompt = Prompt(
        id=uuid4(),
        name=prompt_create.name,
        description=prompt_create.description,
        prompt_template=prompt_create.prompt_template,
        version=prompt_create.version,
        is_active=getattr(prompt_create, 'is_active', True),
        created_at=now,
        updated_at=now
    )
    db.add(new_prompt)
    await db.commit()
    await db.refresh(new_prompt)
    return SchemaPrompt.from_orm(new_prompt)

async def get_prompt_by_id(db: AsyncSession, prompt_id) -> SchemaPrompt | None:
    result = await db.execute(select(Prompt).filter(Prompt.id == prompt_id))
    prompt = result.scalar_one_or_none()
    if prompt:
        return SchemaPrompt.from_orm(prompt)
    return None

async def update_prompt(db: AsyncSession, prompt_id, prompt_update: PromptCreate) -> SchemaPrompt | None:
    result = await db.execute(select(Prompt).filter(Prompt.id == prompt_id))
    prompt = result.scalar_one_or_none()
    if not prompt:
        return None

    for field, value in prompt_update.dict(exclude_unset=True).items():
        setattr(prompt, field, value)
    prompt.updated_at = datetime.utcnow()
    await db.commit()
    await db.refresh(prompt)
    return SchemaPrompt.from_orm(prompt)

async def delete_prompt(db: AsyncSession, prompt_id) -> bool:
    result = await db.execute(select(Prompt).filter(Prompt.id == prompt_id))
    prompt = result.scalar_one_or_none()
    if not prompt:
        return False
    await db.delete(prompt)
    await db.commit()
    return True
