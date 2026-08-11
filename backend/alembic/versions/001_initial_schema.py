"""Initial schema with all tables

Revision ID: 001
Revises: 
Create Date: 2026-08-11 13:41:00.000000
"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy.dialects.postgresql as pg

# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table('users',
        sa.Column('id', pg.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column('email', sa.String(length=320), unique=True, nullable=False, index=True),
        sa.Column('full_name', sa.String(length=255), nullable=False),
        sa.Column('role', sa.String(length=20), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.text('true')),
        sa.Column('hashed_password', sa.String(length=256), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('last_login', sa.DateTime(timezone=True), nullable=True)
    )

    op.create_table('news_sources',
        sa.Column('id', pg.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('source_type', sa.String(length=20), nullable=False),
        sa.Column('url', sa.String(length=1024), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.text('true')),
        sa.Column('country', sa.String(length=20), nullable=True),
        sa.Column('language', sa.String(length=20), nullable=True),
        sa.Column('scrape_pattern', sa.Text(), nullable=True),
        sa.Column('polling_interval_minutes', sa.Integer(), nullable=False, server_default=sa.text('60')),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False)
    )

    op.create_table('news_items',
        sa.Column('id', pg.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column('title', sa.String(length=1024), nullable=False),
        sa.Column('content_summary', sa.Text(), nullable=True),
        sa.Column('full_content', sa.Text(), nullable=True),
        sa.Column('url', sa.String(length=1024), nullable=False),
        sa.Column('source_id', pg.UUID(as_uuid=True), nullable=False),
        sa.Column('country', sa.String(length=20), nullable=False),
        sa.Column('language', sa.String(length=20), nullable=False),
        sa.Column('published_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('is_direct_mention', sa.Boolean(), nullable=False, server_default=sa.text('false')),
        sa.Column('sentiment_score', sa.Float(), nullable=True),
        sa.Column('relevance_score', sa.Float(), nullable=False, server_default=sa.text('0.0')),
        sa.Column('urgency_score', sa.Float(), nullable=False, server_default=sa.text('0.0')),
        sa.Column('impact_score', sa.Float(), nullable=False, server_default=sa.text('0.0')),
        sa.Column('overall_score', sa.Float(), nullable=False, server_default=sa.text('0.0')),
        sa.Column('status', sa.String(length=20), nullable=False, server_default=sa.text('pending')),
        sa.Column('operator_rating', sa.Integer(), nullable=True),
        sa.Column('operator_notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('trace_id', pg.UUID(as_uuid=True), nullable=False),
        sa.Column('prompt_version', sa.String(length=64), nullable=True),
        sa.Column('model_version', sa.String(length=64), nullable=True)
    )

    op.create_table('scoring_dimensions',
        sa.Column('id', pg.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('description', sa.String(length=1024), nullable=False),
        sa.Column('weight', sa.Float(), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.text('true')),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False)
    )

    op.create_table('report_templates',
        sa.Column('id', pg.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('template_content', sa.Text(), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.text('true')),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False)
    )

    op.create_table('reports',
        sa.Column('id', pg.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('template_id', pg.UUID(as_uuid=True), nullable=True),
        sa.Column('country_filter', sa.String(length=64), nullable=True),
        sa.Column('language_filter', sa.String(length=64), nullable=True),
        sa.Column('date_from', sa.DateTime(timezone=True), nullable=True),
        sa.Column('date_to', sa.DateTime(timezone=True), nullable=True),
        sa.Column('min_score', sa.Float(), nullable=True),
        sa.Column('status', sa.String(length=20), nullable=False, server_default=sa.text('draft')),
        sa.Column('content_html', sa.Text(), nullable=True),
        sa.Column('approved_by', pg.UUID(as_uuid=True), nullable=True),
        sa.Column('approved_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('published_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_by', pg.UUID(as_uuid=True), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False)
    )

    op.create_table('notification_recipients',
        sa.Column('id', pg.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('email', sa.String(length=320), nullable=True),
        sa.Column('slack_webhook', sa.String(length=1024), nullable=True),
        sa.Column('webhook_url', sa.String(length=1024), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.text('true')),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False)
    )

    op.create_table('channel_configs',
        sa.Column('id', pg.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('channel_type', sa.String(length=20), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.text('true')),
        sa.Column('config_data', sa.Text(), nullable=False, server_default=sa.text('"{}"')),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False)
    )

    op.create_table('prompts',
        sa.Column('id', pg.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('prompt_template', sa.Text(), nullable=False),
        sa.Column('version', sa.String(length=64), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.text('true')),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False)
    )

    op.create_table('audit_logs',
        sa.Column('id', pg.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column('user_id', pg.UUID(as_uuid=True), nullable=False),
        sa.Column('action', sa.String(length=255), nullable=False),
        sa.Column('resource_type', sa.String(length=255), nullable=False),
        sa.Column('resource_id', pg.UUID(as_uuid=True), nullable=True),
        sa.Column('details', sa.Text(), nullable=True),
        sa.Column('ip_address', sa.String(length=45), nullable=True),
        sa.Column('user_agent', sa.String(length=255), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False)
    )

def downgrade():
    op.drop_table('audit_logs')
    op.drop_table('prompts')
    op.drop_table('channel_configs')
    op.drop_table('notification_recipients')
    op.drop_table('reports')
    op.drop_table('report_templates')
    op.drop_table('scoring_dimensions')
    op.drop_table('news_items')
    op.drop_table('news_sources')
    op.drop_table('users')
