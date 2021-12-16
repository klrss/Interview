"""new migration

Revision ID: 875a6c7274af
Revises: 
Create Date: 2021-12-16 22:50:03.895059

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '875a6c7274af'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('questionary',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.Text(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['useru.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_index('ix_user_email', table_name='useru')
    op.drop_index('ix_user_username', table_name='useru')
    op.create_index(op.f('ix_useru_email'), 'useru', ['email'], unique=False)
    op.create_index(op.f('ix_useru_username'), 'useru', ['username'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_useru_username'), table_name='useru')
    op.drop_index(op.f('ix_useru_email'), table_name='useru')
    op.create_index('ix_user_username', 'useru', ['username'], unique=False)
    op.create_index('ix_user_email', 'useru', ['email'], unique=False)
    op.drop_table('questionary')
    # ### end Alembic commands ###