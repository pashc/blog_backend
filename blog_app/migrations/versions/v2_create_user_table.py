"""empty message

Revision ID: 2d8ac56a4074
Revises: 06d456ae41df
Create Date: 2017-12-25 23:06:49.784495

"""
from alembic import op
import sqlalchemy as sa

revision = '2d8ac56a4074'
down_revision = '06d456ae41df'
branch_labels = None
depends_on = None

USER_ID = sa.schema.Sequence("user_id_seq")


def upgrade():
    op.execute(sa.schema.CreateSequence(USER_ID))
    op.create_table('users',
                    sa.Column('id', sa.Integer(), server_default=sa.text("nextval('user_id_seq')"), nullable=False),
                    sa.Column('username', sa.String(length=32), nullable=True),
                    sa.Column('password_hash', sa.String(length=128), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=False)


def downgrade():
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_table('users')
    op.execute(sa.schema.DropSequence(USER_ID))
