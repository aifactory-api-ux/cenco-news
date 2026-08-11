// src/services/news.service.ts
import api from '../lib/api';
import { NewsItem, NewsItemFilter, NewsItemListResponse } from '../../shared/types';

export async function fetchNews(filter?: NewsItemFilter, page = 1, pageSize = 20): Promise<NewsItemListResponse> {
  // Build query params from filter
  const params: any = { page, page_size: pageSize };
  if (filter) {
    if (filter.status) params.status = filter.status;
    if (filter.source_id) params.source_id = filter.source_id;
    if (filter.country) params.country = filter.country;
    if (filter.language) params.language = filter.language;
    if (filter.is_direct_mention !== undefined) params.is_direct_mention = filter.is_direct_mention;
    if (filter.min_score !== undefined) params.min_score = filter.min_score;
    if (filter.max_score !== undefined) params.max_score = filter.max_score;
    if (filter.start_date) params.start_date = filter.start_date;
    if (filter.end_date) params.end_date = filter.end_date;
    if (filter.search_query) params.search_query = filter.search_query;
  }
  const response = await api.get('/api/v1/news', { params });
  return response.data as NewsItemListResponse;
}

export async function fetchNewsById(id: string): Promise<NewsItem> {
  const response = await api.get(`/api/v1/news/${id}`);
  return response.data as NewsItem;
}
