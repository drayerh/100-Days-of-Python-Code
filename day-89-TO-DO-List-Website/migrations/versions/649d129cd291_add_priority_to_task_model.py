"""Add priority to Task model

Revision ID: 649d129cd291
Revises: 
Create Date: 2025-02-07 18:38:15.622108

"""
# migrations/versions/649d129cd291_add_priority_to_task_model.py

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '649d129cd291'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    with op.batch_alter_table('task', schema=None) as batch_op:
        batch_op.add_column(sa.Column('priority', sa.Integer(), nullable=True))
        # Added constraint name
        batch_op.create_foreign_key('fk_task_user_id', 'user', ['user_id'], ['id'])

def downgrade():
    with op.batch_alter_table('task', schema=None) as batch_op:
        batch_op.drop_constraint('fk_task_user_id', type_='foreignkey')
        batch_op.drop_column('priority')