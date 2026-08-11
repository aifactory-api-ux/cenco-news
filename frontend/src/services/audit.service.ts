// src/services/audit.service.ts
import api from '../lib/api';
import { AuditLog } from '../../shared/types';

interface AuditLogFilter {
  user_id?: string;
  action?: string;
  resource_type?: string;
  resource_id?: string;
  start_date?: string;
  end_date?: string;
  page?: number;
  page_size?: number;
}

export async function fetchAuditLogs(filter?: AuditLogFilter): Promise<{ items: AuditLog[]; total: number; page: number; page_size: number; pages: number }> {
  const params: any = {};
  if (filter) {
    if (filter.user_id) params.user_id = filter.user_id;
    if (filter.action) params.action = filter.action;
    if (filter.resource_type) params.resource_type = filter.resource_type;
    if (filter.resource_id) params.resource_id = filter.resource_id;
    if (filter.start_date) params.start_date = filter.start_date;
    if (filter.end_date) params.end_date = filter.end_date;
    params.page = filter.page || 1;
    params.page_size = filter.page_size || 20;
  }
  const response = await api.get('/api/v1/audit', { params });
  return response.data;
}
