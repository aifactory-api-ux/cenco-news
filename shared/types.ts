export enum UserRole {
  ADMIN = "admin",
  MANAGER = "manager",
  NEWS_OPERATOR = "news_operator",
  VIEWER = "viewer"
}

export interface UserBase {
  email: string;
  full_name: string;
  role: UserRole;
}

export interface UserCreate extends UserBase {
  password: string;
}

export interface UserUpdate {
  email?: string;
  full_name?: string;
  role?: UserRole;
  is_active?: boolean;
}

export interface User {
  id: string;
  is_active: boolean;
  created_at: string;
  updated_at: string;
  last_login?: string;
}

// News related types
export enum NewsSourceType {
  RSS = "rss",
  WEB_SCRAPE = "web_scrape",
  NEWS_API = "news_api"
}

export enum NewsStatus {
  PENDING = "pending",
  REVIEWED = "reviewed",
  APPROVED = "approved",
  REJECTED = "rejected",
  PUBLISHED = "published"
}

export enum Language {
  SPANISH = "es",
  PORTUGUESE = "pt",
  ENGLISH = "en"
}

export enum Country {
  CHILE = "chile",
  ARGENTINA = "argentina",
  BRAZIL = "brazil",
  PERU = "peru",
  COLOMBIA = "colombia",
  URUGUAY = "uruguay"
}

export interface NewsSourceBase {
  name: string;
  source_type: NewsSourceType;
  url: string;
  is_active: boolean;
  country?: Country;
  language?: Language;
  scrape_pattern?: string;
  polling_interval_minutes: number;
}

export interface NewsSourceCreate extends NewsSourceBase {}

export interface NewsSource extends NewsSourceBase {
  id: string;
  created_at: string;
  updated_at: string;
}

export interface NewsItemBase {
  title: string;
  content_summary?: string;
  full_content?: string;
  url: string;
  source_id: string;
  country: Country;
  language: Language;
  published_at?: string;
  is_direct_mention: boolean;
  sentiment_score?: number;
}

export interface NewsItemCreate extends NewsItemBase {
  source_name?: string;
  image_url?: string;
  trace_id: string;
}

export interface NewsItem extends NewsItemBase {
  id: string;
  relevance_score: number;
  urgency_score: number;
  impact_score: number;
  overall_score: number;
  status: NewsStatus;
  operator_rating?: number;
  operator_notes?: string;
  created_at: string;
  updated_at: string;
  trace_id: string;
  prompt_version?: string;
  model_version?: string;
}

export interface NewsItemWithSource extends NewsItem {
  source: NewsSource;
}

export interface NewsItemFilter {
  status?: NewsStatus;
  source_id?: string;
  country?: Country;
  language?: Language;
  is_direct_mention?: boolean;
  min_score?: number;
  max_score?: number;
  start_date?: string;
  end_date?: string;
  search_query?: string;
}

export interface NewsItemListResponse {
  items: NewsItemWithSource[];
  total: number;
  page: number;
  page_size: number;
  pages: number;
}

// Scoring types
export interface ScoringDimensionBase {
  name: string;
  description: string;
  weight: number; // 0 to 1
  is_active: boolean;
}

export interface ScoringDimensionCreate extends ScoringDimensionBase {}

export interface ScoringDimension extends ScoringDimensionBase {
  id: string;
  created_at: string;
  updated_at: string;
}

export interface ScoringWeights {
  relevance_weight: number;
  urgency_weight: number;
  impact_weight: number;
}

// Report types
export enum ReportStatus {
  DRAFT = "draft",
  PENDING_APPROVAL = "pending_approval",
  APPROVED = "approved",
  REJECTED = "rejected",
  PUBLISHED = "published",
  SENT = "sent"
}

export enum ReportFormat {
  PDF = "pdf",
  HTML = "html",
  CSV = "csv"
}

export interface ReportTemplateBase {
  name: string;
  description?: string;
  template_content: string;
  is_active: boolean;
}

export interface ReportTemplateCreate extends ReportTemplateBase {}

export interface ReportTemplate extends ReportTemplateBase {
  id: string;
  created_at: string;
  updated_at: string;
}

export interface ReportBase {
  title: string;
  template_id?: string;
  country_filter?: string;
  language_filter?: string;
  date_from?: string;
  date_to?: string;
  min_score?: number;
  status: ReportStatus;
}

export interface ReportCreate extends ReportBase {
  include_news_ids: string[];
}

export interface Report extends ReportBase {
  id: string;
  content_html?: string;
  approved_by?: string;
  approved_at?: string;
  published_at?: string;
  created_by: string;
  created_at: string;
  updated_at: string;
}

export interface ReportWithNews extends Report {
  news_items: NewsItem[];
}

// Notification types
export enum ChannelType {
  EMAIL = "email",
  SLACK = "slack",
  WEBHOOK = "webhook"
}

export interface NotificationRecipientBase {
  name: string;
  email?: string;
  slack_webhook?: string;
  webhook_url?: string;
  is_active: boolean;
}

export interface NotificationRecipientCreate extends NotificationRecipientBase {}

export interface NotificationRecipient extends NotificationRecipientBase {
  id: string;
  created_at: string;
  updated_at: string;
}

export interface ChannelConfigBase {
  name: string;
  channel_type: ChannelType;
  is_active: boolean;
  config_data: Record<string, any>;
}

export interface ChannelConfigCreate extends ChannelConfigBase {}

export interface ChannelConfig extends ChannelConfigBase {
  id: string;
  created_at: string;
  updated_at: string;
}

// Prompt types
export interface PromptBase {
  name: string;
  description?: string;
  prompt_template: string;
  version: string;
  is_active: boolean;
}

export interface PromptCreate extends PromptBase {}

export interface Prompt extends PromptBase {
  id: string;
  created_at: string;
  updated_at: string;
}

// Audit types
export interface AuditLogBase {
  user_id: string;
  action: string;
  resource_type: string;
  resource_id?: string;
  details?: Record<string, any>;
  ip_address?: string;
  user_agent?: string;
}

export interface AuditLogCreate extends AuditLogBase {}

export interface AuditLog extends AuditLogBase {
  id: string;
  created_at: string;
}

export interface AuditLogFilter {
  user_id?: string;
  action?: string;
  resource_type?: string;
  resource_id?: string;
  start_date?: string;
  end_date?: string;
}

export interface AuditLogListResponse {
  items: AuditLog[];
  total: number;
  page: number;
  page_size: number;
  pages: number;
}
