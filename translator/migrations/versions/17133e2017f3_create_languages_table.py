"""create languages table

Revision ID: 17133e2017f3
Revises: 
Create Date: 2025-04-06 19:33:16.985523

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '17133e2017f3'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        'languages',
        sa.Column('language', sa.String, primary_key=True),
        sa.Column('iso', sa.String(2), unique=True, nullable=False),
    )

def downgrade():
    op.drop_table('languages')