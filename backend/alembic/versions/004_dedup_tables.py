"""create deduplication related tables

Revision ID: 004_dedup_tables
Revises: 003_articles_table
Create Date: 2026-08-11 01:00:00.000000
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '004_dedup_tables'
down_revision = '003_articles_table'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'duplicate_groups',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.func.now(), onupdate=sa.func.now())
    )

    op.create_table(
        'article_embeddings',
        sa.Column('article_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('news_articles.id', ondelete='CASCADE'), primary_key=True, nullable=False),
        sa.Column('embedding', postgresql.ARRAY(sa.Float), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.func.now(), onupdate=sa.func.now())
    )

    # Index for efficient vector search
    op.create_index("ix_article_embeddings_embedding", "article_embeddings", ["embedding"], postgresql_using='gin')


def downgrade():
    op.drop_index("ix_article_embeddings_embedding", table_name='article_embeddings')
    op.drop_table('article_embeddings')
    op.drop_table('duplicate_groups')
