"""add media to post

Revision ID: 75479fdc2248
Revises: ac01f8047f54
Create Date: 2024-09-21 14:16:19.822627

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '75479fdc2248'
down_revision: Union[str, None] = 'ac01f8047f54'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('media', sa.String(length=255), nullable=True))


def downgrade() -> None:
    pass
