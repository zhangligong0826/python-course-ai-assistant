"""add password reset tokens and auth session version

Revision ID: a1b2c3d4e5f7
Revises: f0bd01a18a3d
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = 'a1b2c3d4e5f7'
down_revision: str | None = 'f0bd01a18a3d'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    with op.batch_alter_table('auth') as batch_op:
        batch_op.add_column(sa.Column('session_version', sa.Integer(), nullable=False, server_default='0'))

    op.create_table(
        'password_reset_token',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('user_id', sa.String(), nullable=False),
        sa.Column('token_hash', sa.String(length=64), nullable=False),
        sa.Column('expires_at', sa.BigInteger(), nullable=False),
        sa.Column('used_at', sa.BigInteger(), nullable=True),
        sa.Column('created_at', sa.BigInteger(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('token_hash'),
    )
    op.create_index('ix_password_reset_token_user_id', 'password_reset_token', ['user_id'])
    op.create_index('ix_password_reset_token_token_hash', 'password_reset_token', ['token_hash'], unique=True)


def downgrade() -> None:
    op.drop_index('ix_password_reset_token_token_hash', table_name='password_reset_token')
    op.drop_index('ix_password_reset_token_user_id', table_name='password_reset_token')
    op.drop_table('password_reset_token')
    with op.batch_alter_table('auth') as batch_op:
        batch_op.drop_column('session_version')
