"""Added new project type field to Forest Buffer for urban calculations;

Revision ID: 0231cff71847
Revises: a9716781c042
Create Date: 2016-03-28 10:27:00.756624

"""

# revision identifiers, used by Alembic.
revision = '0231cff71847'
down_revision = 'a9716781c042'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('bmp_forest_buffer', sa.Column('type_of_buffer_project', sa.String))


def downgrade():
    op.drop_column('bmp_forest_buffer', 'type_of_buffer_project')
