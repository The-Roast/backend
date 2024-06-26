"""Created schedule fields and clicks for Digest table.

Revision ID: eb99e7510ea0
Revises: 9c757d500529
Create Date: 2023-08-06 16:29:46.671825

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'eb99e7510ea0'
down_revision = '9c757d500529'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('digest', sa.Column('clicks', sa.Integer(), nullable=False))
    op.add_column('digest', sa.Column('schedule', sa.String(), nullable=False))
    op.create_index(op.f('ix_digest_schedule'), 'digest', ['schedule'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_digest_schedule'), table_name='digest')
    op.drop_column('digest', 'schedule')
    op.drop_column('digest', 'clicks')
    # ### end Alembic commands ###
