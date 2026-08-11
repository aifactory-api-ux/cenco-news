from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from uuid import UUID

from backend.src.schemas.notification import (
    NotificationRecipient, NotificationRecipientCreate, ChannelConfig, ChannelConfigCreate
)
from backend.src.services.notification_service import (
    list_recipients,
    create_recipient,
    get_recipient_by_id,
    update_recipient,
    delete_recipient,
    list_channels,
    create_channel
)
from backend.src.api.deps import get_db, get_current_user
from backend.src.models.user import User

router = APIRouter(prefix="/notifications", tags=["notifications"])

@router.get("/recipients", response_model=List[NotificationRecipient])
async def get_recipients(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    recipients = await list_recipients(db)
    return recipients

@router.post("/recipients", response_model=NotificationRecipient, status_code=status.HTTP_201_CREATED)
async def post_recipient(
    recipient_create: NotificationRecipientCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    recipient = await create_recipient(db, recipient_create)
    return recipient

@router.get("/recipients/{recipient_id}", response_model=NotificationRecipient)
async def get_recipient(
    recipient_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    recipient = await get_recipient_by_id(db, recipient_id)
    if not recipient:
        raise HTTPException(status_code=404, detail="Destinatario no encontrado")
    return recipient

@router.put("/recipients/{recipient_id}", response_model=NotificationRecipient)
async def put_recipient(
    recipient_id: UUID,
    recipient_update: NotificationRecipientCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    updated = await update_recipient(db, recipient_id, recipient_update)
    if not updated:
        raise HTTPException(status_code=404, detail="Destinatario no encontrado para actualizar")
    return updated

@router.delete("/recipients/{recipient_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_recipient_route(
    recipient_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    deleted = await delete_recipient(db, recipient_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Destinatario no encontrado para eliminar")

@router.get("/channels", response_model=List[ChannelConfig])
async def get_channels(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    channels = await list_channels(db)
    return channels

@router.post("/channels", response_model=ChannelConfig, status_code=status.HTTP_201_CREATED)
async def post_channel(
    channel_create: ChannelConfigCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    channel = await create_channel(db, channel_create)
    return channel
