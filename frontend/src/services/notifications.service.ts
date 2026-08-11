// src/services/notifications.service.ts
import api from '../lib/api';
import { NotificationRecipient, ChannelConfig } from '../../shared/types';

export async function fetchNotificationRecipients(): Promise<NotificationRecipient[]> {
  const response = await api.get('/api/v1/notifications/recipients');
  return response.data.items as NotificationRecipient[];
}

export async function createNotificationRecipient(recipient: NotificationRecipient): Promise<NotificationRecipient> {
  const response = await api.post('/api/v1/notifications/recipients', recipient);
  return response.data as NotificationRecipient;
}

export async function fetchChannelConfigs(): Promise<ChannelConfig[]> {
  const response = await api.get('/api/v1/notifications/channels');
  return response.data.items as ChannelConfig[];
}

export async function createChannelConfig(config: ChannelConfig): Promise<ChannelConfig> {
  const response = await api.post('/api/v1/notifications/channels', config);
  return response.data as ChannelConfig;
}
