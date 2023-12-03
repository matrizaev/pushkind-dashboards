"""empty message

Revision ID: 499882080a75
Revises: 015f627bc466
Create Date: 2023-12-02 15:18:24.882570

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '499882080a75'
down_revision = '015f627bc466'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('picture', sa.String(length=128), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('picture')

    # ### end Alembic commands ###
