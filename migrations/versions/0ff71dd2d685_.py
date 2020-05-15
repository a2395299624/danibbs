"""empty message

Revision ID: 0ff71dd2d685
Revises: 626ada155518
Create Date: 2020-05-13 18:50:13.309662

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '0ff71dd2d685'
down_revision = '626ada155518'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.add_column(sa.Column('read_num', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('top', sa.Boolean(), nullable=True))
        batch_op.drop_column('highlight')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.add_column(sa.Column('highlight', mysql.TINYINT(display_width=1), autoincrement=False, nullable=True))
        batch_op.drop_column('top')
        batch_op.drop_column('read_num')

    # ### end Alembic commands ###
