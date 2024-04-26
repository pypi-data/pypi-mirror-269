"""Add severity to Task and add severity level UNKNOWN

Revision ID: e99bc35702c9
Revises: 7d480e6f1112
Create Date: 2024-02-28 14:14:22.519918

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision: str = "e99bc35702c9"
down_revision: Union[str, None] = "7d480e6f1112"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    bind = op.get_bind()
    if bind.engine.name != "sqlite":
        op.execute("ALTER TYPE severity ADD VALUE 'unknown'")
    op.add_column(
        "tasks",
        sa.Column(
            "severity",
            sa.Enum("ok", "warning", "critical", "unknown", name="severity"),
            nullable=False,
        ),
    )
    op.add_column(
        "tasks", sa.Column("last_severity_update", sa.DateTime(), nullable=True)
    )


def downgrade() -> None:
    op.drop_column("tasks", "last_severity_update")
    op.drop_column("tasks", "severity")
