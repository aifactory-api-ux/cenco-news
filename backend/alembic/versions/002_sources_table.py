"""create sources table

Revision ID: 002_sources_table
Revises: 001_initial_schema
Create Date: 2026-08-11 01:30:00.000000
"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy.dialects.postgresql as pg

# revision identifiers, used by Alembic.
revision = '002_sources_table'
down_revision = '001_initial_schema'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'sources',
        sa.Column('id', pg.UUID(as_uuid=True), primary_key=True, default=sa.text('gen_random_uuid()')),
        sa.Column('name', sa.String, nullable=False),
        sa.Column('type', sa.Enum('rss', 'api', 'scraper', name='sourcetype'), nullable=False),
        sa.Column('url', sa.String, nullable=False),
        sa.Column('priority', sa.Integer, default=1),
        sa.Column('country', sa.String, nullable=False),
        sa.Column('language', sa.Enum('es', 'pt', 'en', name='language'), nullable=False),
        sa.Column('status', sa.Enum('active', 'inactive', 'error', 'maintenance', name='sourcestatus'), nullable=False, server_default='active'),
        sa.Column('adapter_config', sa.Text, default='{}'),
        sa.Column('last_fetch_at', sa.DateTime, nullable=True),
        sa.Column('last_error', sa.String, nullable=True),
        sa.Column('error_count', sa.Integer, default=0),
        sa.Column('is_enabled', sa.Boolean, default=True),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime, server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False)
    )


def downgrade():
    op.drop_table('sources')
    sa.Enum(name='sourcetype').drop(op.get_bind())
    sa.Enum(name='language').drop(op.get_bind())
    sa.Enum(name='sourcestatus').drop(op.get_bind())
