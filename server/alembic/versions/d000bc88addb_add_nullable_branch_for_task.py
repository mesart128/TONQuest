"""add nullable branch for task

Revision ID: d000bc88addb
Revises: 63fb0db813b7
Create Date: 2024-11-21 22:30:06.828958

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd000bc88addb'
down_revision: Union[str, None] = '63fb0db813b7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('slides', 'title',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('slides', 'description',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('slides', 'image',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('tasks', 'branch_id',
               existing_type=sa.UUID(),
               nullable=True)
    op.alter_column('users', 'username',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('users', 'last_name',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('users', 'image',
               existing_type=sa.VARCHAR(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'image',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('users', 'last_name',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('users', 'username',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('tasks', 'branch_id',
               existing_type=sa.UUID(),
               nullable=False)
    op.alter_column('slides', 'image',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('slides', 'description',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('slides', 'title',
               existing_type=sa.VARCHAR(),
               nullable=False)
    # ### end Alembic commands ###
