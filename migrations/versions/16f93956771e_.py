"""empty message

Revision ID: 16f93956771e
Revises: 
Create Date: 2023-12-13 20:05:07.642986

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '16f93956771e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('nombre', sa.String(length=100), nullable=True),
    sa.Column('email', sa.String(length=100), nullable=False),
    sa.Column('password', sa.String(length=100), nullable=True),
    sa.Column('rut_compania', sa.Integer(), nullable=True),
    sa.Column('compania_local', sa.LargeBinary(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    # ### end Alembic commands ###