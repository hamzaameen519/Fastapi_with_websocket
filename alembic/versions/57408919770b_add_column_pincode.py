"""add column pincode

Revision ID: 57408919770b
Revises: 
Create Date: 2024-10-01 15:11:00.506413

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '57408919770b'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("users",sa.Column('pincode', sa.String(30)),)


def downgrade() -> None:
    op.drop_column("users",'pincode')
