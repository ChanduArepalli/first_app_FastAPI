"""Add a column

Revision ID: 4c319a3e531d
Revises: 
Create Date: 2022-07-23 00:36:08.120739

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4c319a3e531d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True, unique=True),
        sa.Column('username', sa.String(255), unique=True),
        sa.Column('hashed_password', sa.String(255)),
        sa.Column('first_name', sa.String(255), nullable=True),
        sa.Column('last_name', sa.String(255), nullable=True),
        sa.Column('is_active', sa.Boolean, default=True),
        sa.Column('created_at', sa.DateTime, nullable=True),
    )


def downgrade() -> None:
    pass
