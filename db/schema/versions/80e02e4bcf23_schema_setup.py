"""schema setup

Revision ID: 80e02e4bcf23
Revises:
Create Date: 2025-01-09 23:31:40.398433

"""

from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "80e02e4bcf23"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("CREATE SCHEMA recipe_data")
    pass


def downgrade() -> None:
    op.execute("DROP SCHEMA recipe_data CASCADE")
    pass
