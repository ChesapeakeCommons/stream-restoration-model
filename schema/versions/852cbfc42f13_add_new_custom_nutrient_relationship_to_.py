"""Add new custom Nutrient relationship to the Grass Buffer practice

Revision ID: 852cbfc42f13
Revises: 0527c9970506
Create Date: 2018-04-10 11:47:47.858005

"""

# revision identifiers, used by Alembic.
revision = '852cbfc42f13'
down_revision = '0527c9970506'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('bmp_grass_buffer', sa.Column('custom_nutrient_reductions_id', sa.Integer, sa.ForeignKey('nutrient.id')))


def downgrade():
    op.drop_column('bmp_grass_buffer', 'custom_nutrient_reductions_id')
