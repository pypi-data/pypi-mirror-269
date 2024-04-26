"""Adding ConfigCache model

Revision ID: 1a3497f9f71b
Revises: e99bc35702c9
Create Date: 2024-03-13 15:28:09.185377

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision: str = "1a3497f9f71b"
down_revision: Union[str, None] = "e99bc35702c9"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "config_cache",
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("val", sa.String(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("name"),
    )


def downgrade() -> None:
    op.drop_table("config_cache")
