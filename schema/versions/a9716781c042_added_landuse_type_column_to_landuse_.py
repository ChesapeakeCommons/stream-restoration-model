"""Added Landuse Type column to Landuse model

Revision ID: a9716781c042
Revises:
Create Date: 2016-03-17 15:35:17.356150

"""

# revision identifiers, used by Alembic.
revision = 'a9716781c042'
down_revision = None
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('landuse', sa.Column('landuse_type', sa.String))


def downgrade():
    op.drop_column('landuse', 'landuse_type')
