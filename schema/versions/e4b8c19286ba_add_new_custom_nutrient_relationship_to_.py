"""Add new custom nutrient relationship to remaining 9 practices

Revision ID: e4b8c19286ba
Revises: 27d80e7ae234
Create Date: 2018-04-19 13:21:54.178993

"""

# revision identifiers, used by Alembic.
revision = 'e4b8c19286ba'
down_revision = '27d80e7ae234'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('bmp_agriculture_generic', sa.Column('custom_nutrient_reductions_id', sa.Integer, sa.ForeignKey('nutrient.id')))
    op.add_column('bmp_bank_stabilization', sa.Column('custom_nutrient_reductions_id', sa.Integer, sa.ForeignKey('nutrient.id')))
    op.add_column('bmp_bioretention', sa.Column('custom_nutrient_reductions_id', sa.Integer, sa.ForeignKey('nutrient.id')))
    op.add_column('bmp_enhanced_stream_restoration', sa.Column('custom_nutrient_reductions_id', sa.Integer, sa.ForeignKey('nutrient.id')))
    op.add_column('bmp_livestock_exclusion', sa.Column('custom_nutrient_reductions_id', sa.Integer, sa.ForeignKey('nutrient.id')))
    op.add_column('bmp_shoreline_management', sa.Column('custom_nutrient_reductions_id', sa.Integer, sa.ForeignKey('nutrient.id')))
    op.add_column('bmp_stormwater', sa.Column('custom_nutrient_reductions_id', sa.Integer, sa.ForeignKey('nutrient.id')))
    op.add_column('bmp_urban_homeowner', sa.Column('custom_nutrient_reductions_id', sa.Integer, sa.ForeignKey('nutrient.id')))
    op.add_column('bmp_wetlands_nontidal', sa.Column('custom_nutrient_reductions_id', sa.Integer, sa.ForeignKey('nutrient.id')))


def downgrade():
    op.drop_column('bmp_agriculture_generic', 'custom_nutrient_reductions_id')
    op.drop_column('bmp_bank_stabilization', 'custom_nutrient_reductions_id')
    op.drop_column('bmp_bioretention', 'custom_nutrient_reductions_id')
    op.drop_column('bmp_enhanced_stream_restoration', 'custom_nutrient_reductions_id')
    op.drop_column('bmp_livestock_exclusion', 'custom_nutrient_reductions_id')
    op.drop_column('bmp_shoreline_management', 'custom_nutrient_reductions_id')
    op.drop_column('bmp_stormwater', 'custom_nutrient_reductions_id')
    op.drop_column('bmp_urban_homeowner', 'custom_nutrient_reductions_id')
    op.drop_column('bmp_wetlands_nontidal', 'custom_nutrient_reductions_id')
