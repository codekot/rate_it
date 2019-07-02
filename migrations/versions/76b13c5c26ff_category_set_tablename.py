"""category set tablename

Revision ID: 76b13c5c26ff
Revises: 0515cc2c9071
Create Date: 2019-07-02 17:17:48.634723

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '76b13c5c26ff'
down_revision = '0515cc2c9071'
branch_labels = None
depends_on = None


def upgrade():
    op.rename_table('category_model', 'category')


def downgrade():
    op.rename_table('category', 'category_model')
