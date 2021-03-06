"""empty message

Revision ID: 626ada155518
Revises: 9f3b3ef8c63e
Create Date: 2020-05-13 02:51:58.414588

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '626ada155518'
down_revision = '9f3b3ef8c63e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.add_column(sa.Column('highlight', sa.Boolean(), nullable=True))
        batch_op.add_column(sa.Column('recommend', sa.Boolean(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.drop_column('recommend')
        batch_op.drop_column('highlight')

    # ### end Alembic commands ###
