"""adding remaining colomns in the posts

Revision ID: 3385b8a323cb
Revises: ad9dd4a8166a
Create Date: 2026-03-26 23:09:49.363331

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3385b8a323cb'
down_revision: Union[str, Sequence[str], None] = 'ad9dd4a8166a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
def upgrade():
    op.add_column(
        'posts',
        sa.Column(
            'published',
            sa.Boolean(),
            server_default=sa.text('False'),
            nullable=False
        )
    )

    op.add_column(
        'posts',
        sa.Column(
            'created_at',
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text('now()'),
            nullable=False
        )
    )
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('posts','created_at')
    op.drop_column('posts','published')
    pass
