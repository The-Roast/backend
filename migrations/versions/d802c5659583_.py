"""empty message

Revision ID: d802c5659583
Revises: b1d6221773ff
Create Date: 2023-06-17 19:44:13.012930

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd802c5659583'
down_revision = 'b1d6221773ff'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('digests', schema=None) as batch_op:
        batch_op.add_column(sa.Column('uuid', sa.UUID(), nullable=False))
        batch_op.alter_column('name',
               existing_type=sa.VARCHAR(),
               nullable=True)
        batch_op.drop_constraint('digests_name_key', type_='unique')
        batch_op.create_unique_constraint(None, ['uuid'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('digests', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')
        batch_op.create_unique_constraint('digests_name_key', ['name'])
        batch_op.alter_column('name',
               existing_type=sa.VARCHAR(),
               nullable=False)
        batch_op.drop_column('uuid')

    # ### end Alembic commands ###
