"""empty message

Revision ID: 6021bd0e26e0
Revises: 3c7353a715a3
Create Date: 2021-12-21 22:45:28.174668

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6021bd0e26e0'
down_revision = '3c7353a715a3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('useru', sa.Column('role', sa.Integer(), nullable=True))
    op.drop_constraint('user_role_id_fkey', 'useru', type_='foreignkey')
    op.create_foreign_key(None, 'useru', 'role', ['role'], ['id'])
    op.drop_column('useru', 'role_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('useru', sa.Column('role_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'useru', type_='foreignkey')
    op.create_foreign_key('user_role_id_fkey', 'useru', 'role', ['role_id'], ['id'])
    op.drop_column('useru', 'role')
    # ### end Alembic commands ###