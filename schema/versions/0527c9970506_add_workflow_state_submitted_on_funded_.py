"""Add workflow_state, submitted_on, funded_on, and completed_on fields

Revision ID: 0527c9970506
Revises: 0231cff71847
Create Date: 2017-02-28 08:50:12.955409

"""

# revision identifiers, used by Alembic.
revision = '0527c9970506'
down_revision = '0231cff71847'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


"""Example:

1. ALTER TABLE project ADD COLUMN workflow_state text
2. ALTER TABLE project ADD COLUMN submitted_on timestamp
3. ALTER TABLE project ADD COLUMN funded_on timestamp
4. ALTER TABLE project ADD COLUMN completed_on timestamp

"""

def upgrade():
    op.add_column('project', sa.Column('workflow_state', sa.Text))
    op.add_column('project', sa.Column('submitted_on', sa.Timestamp))
    op.add_column('project', sa.Column('funded_on', sa.Timestamp))
    op.add_column('project', sa.Column('completed_on', sa.Timestamp))


def downgrade():
    op.drop_column('project', 'workflow_state')
    op.drop_column('project', 'submitted_on')
    op.drop_column('project', 'funded_on')
    op.drop_column('project', 'completed_on')
