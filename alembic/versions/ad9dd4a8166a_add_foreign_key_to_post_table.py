"""add foreign key to post table

Revision ID: ad9dd4a8166a
Revises: 1693507c7cfc
Create Date: 2026-03-26 22:50:42.171437

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ad9dd4a8166a'
down_revision: Union[str, Sequence[str], None] = '1693507c7cfc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts',sa.Column('owner_id',sa.Integer(),nullable=True))
    op.create_foreign_key('posts_user_fk',source_table='posts',referent_table='users',local_cols=['owner_id'],remote_cols=['id'],ondelete="CASCADE")
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint('posts_user_fk',table_name='posts')
    op.drop_column('owner_id',table_name='posts')
    pass
