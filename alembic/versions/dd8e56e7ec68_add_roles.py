"""add roles

Revision ID: dd8e56e7ec68
Revises: 228c22670c67
Create Date: 2022-11-11 21:53:29.375798

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import table, column, Integer, String

# revision identifiers, used by Alembic.
revision = 'dd8e56e7ec68'
down_revision = '228c22670c67'
branch_labels = None
depends_on = None


def upgrade() -> None:
    roles_table = table(
        'roles',
        column('role_id', Integer),
        column('role_name', String),
    )
    op.bulk_insert(
        roles_table,
        [
            {
                'role_id': 1,
                'role_name': 'moderator'
            },
            {
                'role_id': 0,
                'role_name': 'trainee'
            },
        ]
    )


def downgrade() -> None:
    op.execute('DELETE FROM roles;')
