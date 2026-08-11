from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from uuid import uuid4
from datetime import datetime
import json

from backend.src.models.notification import NotificationRecipient, ChannelConfig
from backend.src.schemas.notification import NotificationRecipientCreate, NotificationRecipient as SchemaRecipient, ChannelConfigCreate, ChannelConfig as SchemaChannel

async def list_recipients(db: AsyncSession) -> List[SchemaRecipient]:
    result = await db.execute(select(NotificationRecipient).filter(NotificationRecipient.is_active == True))
    recipients = result.scalars().all()
    return [SchemaRecipient.from_orm(r) for r in recipients]

async def create_recipient(db: AsyncSession, recipient_create: NotificationRecipientCreate) -> SchemaRecipient:
    now = datetime.utcnow()
    new_recipient = NotificationRecipient(
        id=uuid4(),
        name=recipient_create.name,
        email=recipient_create.email,
        slack_webhook=recipient_create.slack_webhook,
        webhook_url=recipient_create.webhook_url,
        is_active=getattr(recipient_create, 'is_active', True),
        created_at=now,
        updated_at=now
    )
    db.add(new_recipient)
    await db.commit()
    await db.refresh(new_recipient)
    return SchemaRecipient.from_orm(new_recipient)

async def get_recipient_by_id(db: AsyncSession, recipient_id) -> SchemaRecipient | None:
    result = await db.execute(select(NotificationRecipient).filter(NotificationRecipient.id == recipient_id))
    recipient = result.scalar_one_or_none()
    if recipient:
        return SchemaRecipient.from_orm(recipient)
    return None

async def update_recipient(db: AsyncSession, recipient_id, recipient_update: NotificationRecipientCreate) -> SchemaRecipient | None:
    result = await db.execute(select(NotificationRecipient).filter(NotificationRecipient.id == recipient_id))
    recipient = result.scalar_one_or_none()
    if not recipient:
        return None

    for field, value in recipient_update.dict(exclude_unset=True).items():
        setattr(recipient, field, value)
    recipient.updated_at = datetime.utcnow()
    await db.commit()
    await db.refresh(recipient)
    return SchemaRecipient.from_orm(recipient)

async def delete_recipient(db: AsyncSession, recipient_id) -> bool:
    result = await db.execute(select(NotificationRecipient).filter(NotificationRecipient.id == recipient_id))
    recipient = result.scalar_one_or_none()
    if not recipient:
        return False
    await db.delete(recipient)
    await db.commit()
    return True

async def list_channels(db: AsyncSession) -> List[SchemaChannel]:
    result = await db.execute(select(ChannelConfig).filter(ChannelConfig.is_active == True))
    channels = result.scalars().all()
    return [SchemaChannel.from_orm(c) for c in channels]

async def create_channel(db: AsyncSession, channel_create: ChannelConfigCreate) -> SchemaChannel:
    now = datetime.utcnow()
    new_channel = ChannelConfig(
        id=uuid4(),
        name=channel_create.name,
        channel_type=channel_create.channel_type,
        is_active=getattr(channel_create, 'is_active', True),
        config_data=json.dumps(channel_create.config_data) if channel_create.config_data else '{}',
        created_at=now,
        updated_at=now
    )
    db.add(new_channel)
    await db.commit()
    await db.refresh(new_channel)
    return SchemaChannel.from_orm(new_channel)
