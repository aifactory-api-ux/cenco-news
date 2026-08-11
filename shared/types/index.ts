// shared/types/index.ts

import { UUID, HttpUrl, EmailStr } from './primitives';
import { EditorialStatus, SourceType, ReportStatus, Language } from './enums';

export interface NewsArticle {
  id: string; // UUID
  trace_id: string; // UUID
  source_id: string; // UUID
  source_name: string;
  source_type: SourceType;
  url: string; // HttpUrl
  title: string;
  content: string;
  summary?: string;
  author?: string;
  published_at: string; // ISO datetime string
  fetched_at: string; // ISO datetime string
  country: string;
  language: Language;
  entities: string[];
  categories: string[];
  keywords: string[];
  relevance_score: number;
  urgency_score: number;
  impact_score: number;
  overall_score: number;
  duplicate_group_id?: string; // UUID
  is_duplicate: boolean;
  duplicate_of_id?: string; // UUID
  status: EditorialStatus;
  editor_rating?: number;
  editor_feedback?: string;
  approved_by?: string; // UUID
  approved_at?: string; // ISO datetime string
  prompt_version: string;
  model_version: string;
  created_at: string; // ISO datetime string
  updated_at: string; // ISO datetime string
  deleted_at?: string; // ISO datetime string
}

export interface Source {
  id: string; // UUID
  name: string;
  type: SourceType;
  url: string; // HttpUrl
  priority: number;
  country: string;
  language: Language;
  status: string;
  adapter_config: Record<string, any>;
  last_fetch_at?: string; // ISO datetime string
  last_error?: string;
  error_count: number;
  is_enabled: boolean;
  created_at: string; // ISO datetime string
  updated_at: string; // ISO datetime string
}

export interface Report {
  id: string; // UUID
  title: string;
  country: string;
  business_unit: string;
  language: Language;
  status: ReportStatus;
  date_range_start: string; // ISO date string
  date_range_end: string; // ISO date string
  articles: string[]; // UUID[]
  summary?: string;
  generated_at: string; // ISO datetime string
  published_at?: string; // ISO datetime string
  distributed_at?: string; // ISO datetime string
  prompt_version: string;
  model_version: string;
  trace_id: string; // UUID
  created_by: string; // UUID
  approved_by?: string; // UUID
  approved_at?: string; // ISO datetime string
  revision_history: ReportRevision[];
  created_at: string; // ISO datetime string
  updated_at: string; // ISO datetime string
}

export interface ReportRevision {
  id: string; // UUID
  report_id: string; // UUID
  revision_number: number;
  changes_description: string;
  changed_by: string; // UUID
  created_at: string; // ISO datetime string
}

export interface Template {
  id: string; // UUID
  name: string;
  business_unit: string;
  language: Language;
  template_type: string;
  content: string;
  css_styles?: string;
  is_default: boolean;
  created_at: string; // ISO datetime string
  updated_at: string; // ISO datetime string
}

export interface Recipient {
  id: string; // UUID
  email: string; // EmailStr
  name: string;
  business_unit: string;
  country?: string;
  language: Language;
  distribution_list_id: string; // UUID
  is_active: boolean;
  created_at: string; // ISO datetime string
  updated_at: string; // ISO datetime string
}

export interface DistributionList {
  id: string; // UUID
  name: string;
  description?: string;
  business_unit: string;
  country?: string;
  recipients: Recipient[];
  created_at: string; // ISO datetime string
  updated_at: string; // ISO datetime string
}

export interface User {
  id: string; // UUID
  email: string; // EmailStr
  name: string;
  role: string;
  business_unit?: string;
  country?: string;
  language_preference: Language;
  is_active: boolean;
  last_login_at?: string; // ISO datetime string
  created_at: string; // ISO datetime string
  updated_at: string; // ISO datetime string
}
