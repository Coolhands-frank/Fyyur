"""empty message

Revision ID: f285ca02e472
Revises: eb8ea6f3e95f
Create Date: 2022-08-19 12:49:49.739315

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f285ca02e472'
down_revision = 'eb8ea6f3e95f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Artist', sa.Column('seeking_venue', sa.Boolean(), nullable=True))
    op.execute('UPDATE "Artist" SET seeking_venue = False WHERE seeking_venue IS NULL;')
    op.alter_column('Artist', 'seeking_venue', nullable=False)
    op.drop_column('Artist', 'seeking_talent')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Artist', sa.Column('seeking_talent', sa.BOOLEAN(), autoincrement=False, nullable=False))
    op.drop_column('Artist', 'seeking_venue')
    # ### end Alembic commands ###
