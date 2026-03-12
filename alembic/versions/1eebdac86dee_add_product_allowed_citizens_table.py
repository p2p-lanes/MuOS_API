"""add product_allowed_citizens table

Revision ID: 1eebdac86dee
Revises: 2f75e1a8e3a9
Create Date: 2026-02-13 16:13:56.660444

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1eebdac86dee'
down_revision: Union[str, Sequence[str], None] = '2f75e1a8e3a9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'product_allowed_citizens',
        sa.Column(
            'product_id', sa.Integer(), sa.ForeignKey('products.id'), nullable=False
        ),
        sa.Column(
            'citizen_id', sa.Integer(), sa.ForeignKey('humans.id'), nullable=False
        ),
        sa.PrimaryKeyConstraint('product_id', 'citizen_id'),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('product_allowed_citizens')
