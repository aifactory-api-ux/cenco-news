"""create approvals and audit_logs tables

Revision ID: 006
Revises: 005
Create Date: 2026-08-11 00:00:00.000000
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '006'
down_revision = '005'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'approvals',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column('article_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('editor_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('rating', sa.Integer, nullable=False),
        sa.Column('feedback', sa.Text, nullable=True),
        sa.Column('status', sa.Enum('pending', 'approved', 'rejected', name='editorialstatus'), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=False), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(['article_id'], ['news_articles.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['editor_id'], ['users.id'], ondelete='CASCADE'),
    )

    op.create_table(
        'audit_logs',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column('event_type', sa.String(length=50), nullable=False),
        sa.Column('entity_type', sa.String(length=50), nullable=False),
        sa.Column('entity_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('action', sa.String(length=100), nullable=False),
        sa.Column('changes', sa.JSON, nullable=True),
        sa.Column('old_values', sa.JSON, nullable=True),
        sa.Column('new_values', sa.JSON, nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=False), server_default=sa.func.now(), nullable=False),
    )


def downgrade():
    op.drop_table('audit_logs')
    op.drop_table('approvals')
    sa.Enum(name='editorialstatus').drop(op.get_bind(), checkfirst=False)
