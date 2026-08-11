"""create reports table

Revision ID: 005_reports_table
Revises: 004_dedup_tables
Create Date: 2026-08-11 02:00:00.000000
"""

from alembic import op
import sqlalchemy as sa
import sqlalchemy.dialects.postgresql as pg

# revision identifiers, used by Alembic.
revision = '005_reports_table'
down_revision = '004_dedup_tables'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'reports',
        sa.Column('id', pg.UUID(as_uuid=True), primary_key=True, default=sa.text('uuid_generate_v4()')),
        sa.Column('title', sa.String, nullable=False),
        sa.Column('country', sa.String, nullable=False),
        sa.Column('business_unit', sa.String, nullable=False),
        sa.Column('language', sa.String, nullable=False),
        sa.Column('status', sa.String, nullable=False, default='draft'),
        sa.Column('date_range_start', sa.Date, nullable=False),
        sa.Column('date_range_end', sa.Date, nullable=False),
        sa.Column('articles', pg.ARRAY(pg.UUID(as_uuid=True)), nullable=False, default=[]),
        sa.Column('summary', sa.Text, nullable=True),
        sa.Column('generated_at', sa.DateTime, nullable=False),
        sa.Column('published_at', sa.DateTime, nullable=True),
        sa.Column('distributed_at', sa.DateTime, nullable=True),
        sa.Column('prompt_version', sa.String, nullable=False),
        sa.Column('model_version', sa.String, nullable=False),
        sa.Column('trace_id', pg.UUID(as_uuid=True), nullable=False),
        sa.Column('created_by', pg.UUID(as_uuid=True), nullable=False),
        sa.Column('approved_by', pg.UUID(as_uuid=True), nullable=True),
        sa.Column('approved_at', sa.DateTime, nullable=True),
        sa.Column('revision_history', pg.JSONB, nullable=False, default='[]'),
        sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime, nullable=False, server_default=sa.func.now(), onupdate=sa.func.now()),
    )


def downgrade():
    op.drop_table('reports')
