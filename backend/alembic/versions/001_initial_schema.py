"""
Initial database schema for CENCO NEWS
"""

from alembic import op
import sqlalchemy as sa
import sqlalchemy.dialects.postgresql as pg

def upgrade():
    # Users table
    op.create_table(
        'users',
        sa.Column('id', pg.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False, unique=True),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('role', sa.String(length=50), nullable=False),
        sa.Column('business_unit', sa.String(length=255), nullable=True),
        sa.Column('country', sa.String(length=255), nullable=True),
        sa.Column('language_preference', sa.Enum('es', 'pt', 'en', name='language'), nullable=False, server_default='es'),
        sa.Column('password_hash', sa.String(length=255), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('last_login_at', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.func.now(), onupdate=sa.func.now())
    )

    # Roles table (optional, can be simplified if roles are enums)
    op.create_table(
        'roles',
        sa.Column('id', pg.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column('name', sa.String(length=50), nullable=False, unique=True)
    )

def downgrade():
    op.drop_table('roles')
    op.drop_table('users')
