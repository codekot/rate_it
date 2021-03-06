"""user item_view

Revision ID: c7bec20d4d55
Revises: b569ebe8cd58
Create Date: 2019-07-03 17:21:35.184930

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy_utils.types.choice import ChoiceType


# revision identifiers, used by Alembic.
revision = 'c7bec20d4d55'
down_revision = 'b569ebe8cd58'
branch_labels = None
depends_on = None


def upgrade():
    ITEM_VIEWS = [
        ('card', 'card'),
        ('compact', 'compact'),
        ('minimal', 'minimal'),
    ]
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('item_view', ChoiceType(ITEM_VIEWS), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('item_view')

    # ### end Alembic commands ###
