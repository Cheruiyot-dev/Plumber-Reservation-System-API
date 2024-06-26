"""update column character limit

Revision ID: c00259beaec0
Revises: 27bd8cc96b85
Create Date: 2024-04-23 02:12:03.094088

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c00259beaec0'
down_revision = '27bd8cc96b85'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('username',
               existing_type=sa.VARCHAR(length=250),
               type_=sa.String(length=128),
               existing_nullable=False)
        batch_op.alter_column('email',
               existing_type=sa.VARCHAR(length=250),
               type_=sa.String(length=128),
               existing_nullable=False)
        batch_op.alter_column('password',
               existing_type=sa.VARCHAR(length=128),
               type_=sa.String(length=256),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('password',
               existing_type=sa.String(length=256),
               type_=sa.VARCHAR(length=128),
               existing_nullable=False)
        batch_op.alter_column('email',
               existing_type=sa.String(length=128),
               type_=sa.VARCHAR(length=250),
               existing_nullable=False)
        batch_op.alter_column('username',
               existing_type=sa.String(length=128),
               type_=sa.VARCHAR(length=250),
               existing_nullable=False)

    # ### end Alembic commands ###
