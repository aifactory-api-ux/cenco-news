// shared/types/api.ts

import { NewsArticle, Source, Report, User } from './index';
import { EditorialStatus, SourceStatus, Language, ReportStatus } from './enums';

export interface ListSourcesRequest {
  status?: SourceStatus;
  is_enabled?: boolean;
  country?: string;
  language?: Language;
  skip?: number;
  limit?: number;
}

export interface ListSourcesResponse {
  items: Source[];
  total: number;
}

export interface CreateSourceRequest {
  name: string;
  type: string;
  url: string;
  priority?: number;
  country: string;
  language: Language;
  adapter_config?: Record<string, any>;
  is_enabled?: boolean;
}

export interface CreateSourceResponse {
  id: string;
  name: string;
  type: string;
  url: string;
  priority: number;
  country: string;
  language: Language;
  status: string;
  adapter_config: Record<string, any>;
  last_fetch_at?: string;
  last_error?: string;
  error_count: number;
  is_enabled: boolean;
  created_at: string;
  updated_at: string;
}
