from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '38055b07bca6'
down_revision = '649d129cd291'
branch_labels = None
depends_on = None

def upgrade():
    # Drop the temporary table if it exists
    op.execute('DROP TABLE IF EXISTS _alembic_tmp_task')

    with op.batch_alter_table('task', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_id', sa.Integer(), nullable=False, server_default='1'))
        batch_op.create_foreign_key('fk_task_user_id', 'user', ['user_id'], ['id'])

    # Recreate the table without the default value
    op.execute('CREATE TABLE task_new AS SELECT id, content, completed, created_at, priority, user_id FROM task')
    op.execute('DROP TABLE task')
    op.execute('ALTER TABLE task_new RENAME TO task')

    # ### end Alembic commands ###

def downgrade():
    with op.batch_alter_table('task', schema=None) as batch_op:
        batch_op.drop_constraint('fk_task_user_id', type_='foreignkey')
        batch_op.drop_column('user_id')

    # ### end Alembic commands ###