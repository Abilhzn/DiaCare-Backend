"""Add created_at column to users table

Revision ID: 2e03fe0229ca
Revises: 4fedd42f1949
Create Date: 2025-06-13 22:07:42.060086

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2e03fe0229ca'
down_revision = '4fedd42f1949'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('profiles', schema=None) as batch_op:
        batch_op.alter_column('full_name',
               existing_type=sa.VARCHAR(length=120),
               nullable=False)
        batch_op.alter_column('precondition',
               existing_type=sa.VARCHAR(length=50),
               type_=sa.String(length=120),
               existing_nullable=True)
        batch_op.drop_column('updated_at')
        batch_op.drop_column('created_at')

    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('created_at', sa.DateTime(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('created_at')

    with op.batch_alter_table('profiles', schema=None) as batch_op:
        batch_op.add_column(sa.Column('created_at', sa.DATETIME(), nullable=True))
        batch_op.add_column(sa.Column('updated_at', sa.DATETIME(), nullable=True))
        batch_op.alter_column('precondition',
               existing_type=sa.String(length=120),
               type_=sa.VARCHAR(length=50),
               existing_nullable=True)
        batch_op.alter_column('full_name',
               existing_type=sa.VARCHAR(length=120),
               nullable=True)

    # ### end Alembic commands ###
