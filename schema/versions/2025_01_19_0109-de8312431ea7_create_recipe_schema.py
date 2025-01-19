"""create recipe schema

Revision ID: de8312431ea7
Revises:
Create Date: 2025-01-19 01:09:05.665700

"""

from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "de8312431ea7"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("CREATE SCHEMA recipe_data")
    pass


def downgrade() -> None:
    op.execute("DROP SCHEMA recipe_data CASCADE")
    pass
