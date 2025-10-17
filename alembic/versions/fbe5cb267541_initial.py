"""initial

Revision ID: fbe5cb267541
Revises: 
Create Date: 2024-09-13 11:43:23.602777

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fbe5cb267541'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute('create schema core')
    op.create_table('applications',
        sa.Column('client_id', sa.UUID(), nullable=False),
        sa.Column('hashed_client_secret', sa.String(), nullable=False),
        sa.Column('role', sa.Enum('admin', 'user', name='applicationrole'), nullable=False),
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('uuid', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('client_id'),
        sa.UniqueConstraint('uuid'),
        schema='core'
    )
    op.create_index(op.f('ix_core_applications_id'), 'applications', ['id'], unique=True, schema='core')


def downgrade() -> None:
    op.drop_index(op.f('ix_core_applications_id'), table_name='applications', schema='core')
    op.drop_table('applications', schema='core')
    op.execute('drop schema core')
