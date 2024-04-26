"""Initial migrations

Revision ID: 7d480e6f1112
Revises: 
Create Date: 2023-12-16 23:33:40.059077

"""
from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "7d480e6f1112"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "tasks",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("url", sa.String(), nullable=False),
        sa.Column("domain", sa.String(), nullable=False),
        sa.Column("check", sa.String(), nullable=False),
        sa.Column("expected", sa.String(), nullable=False),
        sa.Column("frequency", sa.Integer(), nullable=False),
        sa.Column("selected_by", sa.String(), nullable=True),
        sa.Column("selected_at", sa.DateTime(), nullable=True),
        sa.Column("completed_at", sa.DateTime(), nullable=True),
        sa.Column("next_run", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "results",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("task_id", sa.Integer(), nullable=False),
        sa.Column("agent_id", sa.String(), nullable=True),
        sa.Column("submitted_at", sa.DateTime(), nullable=False),
        sa.Column(
            "status",
            sa.Enum("success", "failure", "error", "on-check", name="status"),
            nullable=False,
        ),
        sa.Column(
            "severity",
            sa.Enum("ok", "warning", "critical", name="severity"),
            nullable=False,
        ),
        sa.Column("context", sa.JSON(), nullable=False),
        sa.ForeignKeyConstraint(
            ["task_id"],
            ["tasks.id"],
            name="results_task_id_fkey",
        ),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("results")
    op.drop_table("tasks")
