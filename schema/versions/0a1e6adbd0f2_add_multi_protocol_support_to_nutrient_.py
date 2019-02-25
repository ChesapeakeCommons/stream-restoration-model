"""Add multi-protocol support to Nutrient data model

Revision ID: 0a1e6adbd0f2
Revises: e4b8c19286ba
Create Date: 2018-04-19 14:05:46.787667

"""

# revision identifiers, used by Alembic.
revision = '0a1e6adbd0f2'
down_revision = 'e4b8c19286ba'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    # op.add_column('nutrient', sa.Column('nitrogen_2', sa.Float(8)))
    # op.add_column('nutrient', sa.Column('phosphorus_2', sa.Float(8)))
    # op.add_column('nutrient', sa.Column('sediment_2', sa.Float(8)))
    pass

def downgrade():
    op.drop_column('nutrient', 'nitrogen_2')
    op.drop_column('nutrient', 'phosphorus_2')
    op.drop_column('nutrient', 'sediment_2')
