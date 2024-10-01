"""add table account

Revision ID: 48940cf9e5ff
Revises: 57408919770b
Create Date: 2024-10-01 15:22:37.377353

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '48940cf9e5ff'
down_revision: Union[str, None] = '57408919770b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('accounts',sa.Column('id', sa.Integer(),primary_key=True),sa.Column('email', sa.String(30),unique=True))


def downgrade() -> None:
    op.drop_table('accounts')
