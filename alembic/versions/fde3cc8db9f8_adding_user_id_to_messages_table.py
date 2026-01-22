"""adding user_id to messages table

Revision ID: fde3cc8db9f8
Revises: 041e536f4a8c
Create Date: 2026-01-19 05:37:03.005669

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fde3cc8db9f8'
down_revision: Union[str, Sequence[str], None] = '041e536f4a8c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. add column
    op.add_column(
        "messages",
        sa.Column("baus_user_id", sa.Integer(), nullable=True),
    )

    # 2. add foreign key
    op.create_foreign_key(
        "fk_messages_baus_user_id_users",
        source_table="messages",
        referent_table="users",
        local_cols=["baus_user_id"],
        remote_cols=["baus_user_id"],
        ondelete="SET NULL",
    )



def downgrade() -> None:
    # drop foreign key first
    op.drop_constraint(
        "fk_messages_user_id_users",
        "messages",
        type_="foreignkey",
    )

    # drop column
    op.drop_column("messages", "user_id")
