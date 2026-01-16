"""drop unique index on raw_message

Revision ID: 041e536f4a8c
Revises: f386d4cffdac
Create Date: 2026-01-16 19:58:26.516363

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '041e536f4a8c'
down_revision: Union[str, Sequence[str], None] = 'f386d4cffdac'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.drop_index(
        'raw_message',
        table_name='messages'
    )

def downgrade():
    op.create_index(
        'raw_message',
        'messages',
        ['raw_message'],
        unique=True
    )