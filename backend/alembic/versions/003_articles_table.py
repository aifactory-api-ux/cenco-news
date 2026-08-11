"""add articles, scoring_rules, prompts tables

Revision ID: 003_articles_table
Revises: 002_sources_table
Create Date: 2026-08-11 03:00:00.000000
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '003_articles_table'
down_revision = '002_sources_table'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'news_articles',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column('trace_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('source_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('sources.id'), nullable=False),
        sa.Column('source_name', sa.String(), nullable=False),
        sa.Column('source_type', sa.Enum('rss', 'api', 'scraper', name='sourcetype'), nullable=False),
        sa.Column('url', sa.String(), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('summary', sa.Text(), nullable=True),
        sa.Column('author', sa.String(), nullable=True),
        sa.Column('published_at', sa.DateTime(), nullable=False),
        sa.Column('fetched_at', sa.DateTime(), nullable=False),
        sa.Column('country', sa.String(), nullable=False),
        sa.Column('language', sa.Enum('es', 'pt', 'en', name='language'), nullable=False),
        sa.Column('entities', sa.Text(), nullable=False, server_default='[]'),
        sa.Column('categories', sa.Text(), nullable=False, server_default='[]'),
        sa.Column('keywords', sa.Text(), nullable=False, server_default='[]'),
        sa.Column('relevance_score', sa.Float(), nullable=False, server_default='0'),
        sa.Column('urgency_score', sa.Float(), nullable=False, server_default='0'),
        sa.Column('impact_score', sa.Float(), nullable=False, server_default='0'),
        sa.Column('overall_score', sa.Float(), nullable=False, server_default='0'),
        sa.Column('duplicate_group_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('is_duplicate', sa.Boolean(), nullable=False, server_default=sa.text('FALSE')),
        sa.Column('duplicate_of_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('status', sa.Enum('pending', 'approved', 'rejected', name='editorialstatus'), nullable=False, server_default='pending'),
        sa.Column('editor_rating', sa.Integer(), nullable=True),
        sa.Column('editor_feedback', sa.Text(), nullable=True),
        sa.Column('approved_by', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('approved_at', sa.DateTime(), nullable=True),
        sa.Column('prompt_version', sa.String(), nullable=False),
        sa.Column('model_version', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('deleted_at', sa.DateTime(), nullable=True),
    )
    
    op.create_table(
        'scoring_rules',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('criteria_json', sa.Text(), nullable=False),
        sa.Column('weight', sa.Float(), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.text('TRUE')),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )

    op.create_table(
        'prompt_templates',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('template_type', sa.String(), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('css_styles', sa.Text(), nullable=True),
        sa.Column('is_default', sa.Boolean(), nullable=False, server_default=sa.text('FALSE')),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )


def downgrade():
    op.drop_table('prompt_templates')
    op.drop_table('scoring_rules')
    op.drop_table('news_articles')

    op.execute('DROP TYPE IF EXISTS editorialstatus')
    op.execute('DROP TYPE IF EXISTS sourcetype')
    op.execute('DROP TYPE IF EXISTS language')
