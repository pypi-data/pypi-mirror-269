"""Add ON DELETE CASCADE to results’ task_id

Revision ID: defda3f2952d
Revises: 1a3497f9f71b
Create Date: 2024-03-18 15:09:34.544573

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "defda3f2952d"
down_revision: Union[str, None] = "1a3497f9f71b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    bind = op.get_bind()
    with op.batch_alter_table("results", schema=None) as batch_op:
        if bind.engine.name != "sqlite":
            batch_op.drop_constraint("results_task_id_fkey", type_="foreignkey")
        batch_op.create_foreign_key(
            "results_task_id_fkey", "tasks", ["task_id"], ["id"], ondelete="CASCADE"
        )


def downgrade() -> None:
    bind = op.get_bind()
    with op.batch_alter_table("results", schema=None) as batch_op:
        if bind.engine.name != "sqlite":
            batch_op.drop_constraint("results_task_id_fkey", type_="foreignkey")
        batch_op.create_foreign_key(
            "results_task_id_fkey", "tasks", ["task_id"], ["id"]
        )
