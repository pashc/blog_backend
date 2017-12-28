"""empty message

Revision ID: 9b0f64ca24be
Revises: 2d8ac56a4074
Create Date: 2017-12-28 01:03:15.065948

"""
from alembic import op
import sqlalchemy as sa


revision = '9b0f64ca24be'
down_revision = '2d8ac56a4074'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('users', sa.Column('email', sa.String(length=64), nullable=True))


def downgrade():
    op.drop_column('users', 'email')
