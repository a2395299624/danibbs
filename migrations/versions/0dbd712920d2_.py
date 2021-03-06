"""empty message

Revision ID: 0dbd712920d2
Revises: 8228d1c51ec0
Create Date: 2020-05-10 21:19:05.920347

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '0dbd712920d2'
down_revision = '8228d1c51ec0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.add_column(sa.Column('author_id', sa.String(length=20), nullable=False))
        batch_op.create_foreign_key(None, 'front_user', ['author_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('author_id')

    # ### end Alembic commands ###
