"""item set tablename

Revision ID: 0515cc2c9071
Revises: eba2a03f6672
Create Date: 2019-07-02 17:12:04.439450

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0515cc2c9071'
down_revision = 'eba2a03f6672'
branch_labels = None
depends_on = None


def upgrade():
    op.rename_table('item_model', 'item')


def downgrade():
    op.rename_table('item', 'item_model')
