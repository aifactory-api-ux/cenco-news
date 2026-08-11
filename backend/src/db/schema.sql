-- CENCO NEWS - Database Schema

-- Users Table
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY NOT NULL,
    email VARCHAR(320) UNIQUE NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    hashed_password VARCHAR(256) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL,
    updated_at TIMESTAMPTZ NOT NULL,
    last_login TIMESTAMPTZ
);

-- News Sources Table
CREATE TABLE IF NOT EXISTS news_sources (
    id UUID PRIMARY KEY NOT NULL,
    name VARCHAR(255) NOT NULL,
    source_type VARCHAR(20) NOT NULL,
    url VARCHAR(1024) NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    country VARCHAR(20),
    language VARCHAR(20),
    scrape_pattern TEXT,
    polling_interval_minutes INTEGER NOT NULL DEFAULT 60,
    created_at TIMESTAMPTZ NOT NULL,
    updated_at TIMESTAMPTZ NOT NULL
);

-- News Items Table
CREATE TABLE IF NOT EXISTS news_items (
    id UUID PRIMARY KEY NOT NULL,
    title VARCHAR(1024) NOT NULL,
    content_summary TEXT,
    full_content TEXT,
    url VARCHAR(1024) NOT NULL,
    source_id UUID NOT NULL REFERENCES news_sources(id),
    country VARCHAR(20) NOT NULL,
    language VARCHAR(20) NOT NULL,
    published_at TIMESTAMPTZ,
    is_direct_mention BOOLEAN NOT NULL DEFAULT FALSE,
    sentiment_score FLOAT,
    relevance_score FLOAT NOT NULL DEFAULT 0.0,
    urgency_score FLOAT NOT NULL DEFAULT 0.0,
    impact_score FLOAT NOT NULL DEFAULT 0.0,
    overall_score FLOAT NOT NULL DEFAULT 0.0,
    status VARCHAR(20) NOT NULL DEFAULT 'pending',
    operator_rating INTEGER,
    operator_notes TEXT,
    created_at TIMESTAMPTZ NOT NULL,
    updated_at TIMESTAMPTZ NOT NULL,
    trace_id UUID NOT NULL,
    prompt_version VARCHAR(64),
    model_version VARCHAR(64)
);

-- Scoring Dimensions Table
CREATE TABLE IF NOT EXISTS scoring_dimensions (
    id UUID PRIMARY KEY NOT NULL,
    name VARCHAR(255) NOT NULL,
    description VARCHAR(1024) NOT NULL,
    weight FLOAT NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL,
    updated_at TIMESTAMPTZ NOT NULL
);

-- Report Templates Table
CREATE TABLE IF NOT EXISTS report_templates (
    id UUID PRIMARY KEY NOT NULL,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    template_content TEXT NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL,
    updated_at TIMESTAMPTZ NOT NULL
);

-- Reports Table
CREATE TABLE IF NOT EXISTS reports (
    id UUID PRIMARY KEY NOT NULL,
    title VARCHAR(255) NOT NULL,
    template_id UUID REFERENCES report_templates(id),
    country_filter VARCHAR(64),
    language_filter VARCHAR(64),
    date_from TIMESTAMPTZ,
    date_to TIMESTAMPTZ,
    min_score FLOAT,
    status VARCHAR(20) NOT NULL DEFAULT 'draft',
    content_html TEXT,
    approved_by UUID,
    approved_at TIMESTAMPTZ,
    published_at TIMESTAMPTZ,
    created_by UUID NOT NULL,
    created_at TIMESTAMPTZ NOT NULL,
    updated_at TIMESTAMPTZ NOT NULL
);

-- Notification Recipients Table
CREATE TABLE IF NOT EXISTS notification_recipients (
    id UUID PRIMARY KEY NOT NULL,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(320),
    slack_webhook VARCHAR(1024),
    webhook_url VARCHAR(1024),
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL,
    updated_at TIMESTAMPTZ NOT NULL
);

-- Channel Configs Table
CREATE TABLE IF NOT EXISTS channel_configs (
    id UUID PRIMARY KEY NOT NULL,
    name VARCHAR(255) NOT NULL,
    channel_type VARCHAR(20) NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    config_data TEXT NOT NULL DEFAULT '{}',
    created_at TIMESTAMPTZ NOT NULL,
    updated_at TIMESTAMPTZ NOT NULL
);

-- Prompts Table
CREATE TABLE IF NOT EXISTS prompts (
    id UUID PRIMARY KEY NOT NULL,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    prompt_template TEXT NOT NULL,
    version VARCHAR(64) NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL,
    updated_at TIMESTAMPTZ NOT NULL
);

-- Audit Logs Table
CREATE TABLE IF NOT EXISTS audit_logs (
    id UUID PRIMARY KEY NOT NULL,
    user_id UUID NOT NULL,
    action VARCHAR(255) NOT NULL,
    resource_type VARCHAR(255) NOT NULL,
    resource_id UUID,
    details TEXT,
    ip_address VARCHAR(45),
    user_agent VARCHAR(255),
    created_at TIMESTAMPTZ NOT NULL
);

-- Sample seed data
-- Insert 3 users
INSERT INTO users (id, email, full_name, role, is_active, hashed_password, created_at, updated_at) VALUES
  ('11111111-1111-1111-1111-111111111111', 'admin@example.com', 'Admin User', 'admin', TRUE, '$2b$12$abcdefghijklmnopqrstuv', NOW(), NOW()),
  ('22222222-2222-2222-2222-222222222222', 'manager@example.com', 'Manager User', 'manager', TRUE, '$2b$12$abcdefghijklmnopqrstuv', NOW(), NOW()),
  ('33333333-3333-3333-3333-333333333333', 'operator@example.com', 'Operator User', 'news_operator', TRUE, '$2b$12$abcdefghijklmnopqrstuv', NOW(), NOW());

-- Insert 2 example news sources
INSERT INTO news_sources (id, name, source_type, url, is_active, country, language, polling_interval_minutes, created_at, updated_at) VALUES
  ('44444444-4444-4444-4444-444444444444', 'Example RSS Feed', 'rss', 'http://example.com/rss', TRUE, 'chile', 'es', 60, NOW(), NOW()),
  ('55555555-5555-5555-5555-555555555555', 'Example Web Scrape', 'web_scrape', 'http://example.com/news', TRUE, 'argentina', 'es', 60, NOW(), NOW());

-- Insert 2 example news items
INSERT INTO news_items (id, title, content_summary, full_content, url, source_id, country, language, published_at, is_direct_mention, relevance_score, urgency_score, impact_score, overall_score, status, created_at, updated_at, trace_id) VALUES
  ('66666666-6666-6666-6666-666666666666', 'Example News Title 1', 'Summary 1', 'Full content 1', 'http://example.com/news/1', '44444444-4444-4444-4444-444444444444', 'chile', 'es', NOW(), FALSE, 0.5, 0.2, 0.3, 0.4, 'pending', NOW(), NOW(), 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa'),
  ('77777777-7777-7777-7777-777777777777', 'Example News Title 2', 'Summary 2', 'Full content 2', 'http://example.com/news/2', '55555555-5555-5555-5555-555555555555', 'argentina', 'es', NOW(), TRUE, 0.7, 0.3, 0.2, 0.5, 'pending', NOW(), NOW(), 'bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb');
