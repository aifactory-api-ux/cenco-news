// src/services/sources.service.ts
import api from '../lib/api';
import { NewsSource, NewsSourceCreate } from '../../shared/types';

export async function fetchSources(): Promise<NewsSource[]> {
  const response = await api.get('/api/v1/sources');
  return response.data.items as NewsSource[];
}

export async function createSource(source: NewsSourceCreate): Promise<NewsSource> {
  const response = await api.post('/api/v1/sources', source);
  return response.data as NewsSource;
}
