"""create schema

Revision ID: 5310fb7c65c6
Revises: 68ae39a9e5ed
Create Date: 2025-01-19 01:02:30.231111
"""

from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "5310fb7c65c6"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("CREATE SCHEMA recipe_data")
    pass


def downgrade() -> None:
    op.execute("DROP SCHEMA recipe_data CASCADE")
    pass
