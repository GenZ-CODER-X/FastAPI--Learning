"""add content column to posts table

Revision ID: e93be3693807
Revises: 62cef4be65b6
Create Date: 2026-03-26 21:46:01.816985

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e93be3693807'
down_revision: Union[str, Sequence[str], None] = '62cef4be65b6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
    'posts',
    sa.Column('content', sa.String(), nullable=False)
)

def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('posts','content')
    pass
