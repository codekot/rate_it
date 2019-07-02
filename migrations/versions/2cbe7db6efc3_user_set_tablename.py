"""user set tablename

Revision ID: 2cbe7db6efc3
Revises: 76b13c5c26ff
Create Date: 2019-07-02 17:18:49.266828

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2cbe7db6efc3'
down_revision = '76b13c5c26ff'
branch_labels = None
depends_on = None


def upgrade():
    op.rename_table('user_model', 'user')


def downgrade():
    op.rename_table('user', 'user_model')
