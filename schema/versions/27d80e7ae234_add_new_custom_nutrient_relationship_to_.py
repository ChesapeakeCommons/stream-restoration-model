"""Add new custom nutrient relationship to Forest Buffer practice

Revision ID: 27d80e7ae234
Revises: 852cbfc42f13
Create Date: 2018-04-19 13:11:29.930634

"""

# revision identifiers, used by Alembic.
revision = '27d80e7ae234'
down_revision = '852cbfc42f13'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('bmp_forest_buffer', sa.Column('custom_nutrient_reductions_id', sa.Integer, sa.ForeignKey('nutrient.id')))


def downgrade():
    op.drop_column('bmp_forest_buffer', 'custom_nutrient_reductions_id')
