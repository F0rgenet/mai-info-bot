"""fix nullable

Revision ID: 031174e3e8d8
Revises: 012ccbc70ffe
Create Date: 2024-11-06 01:52:23.514794

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '031174e3e8d8'
down_revision: Union[str, None] = '012ccbc70ffe'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('groups', 'department',
               existing_type=sa.VARCHAR(length=15),
               nullable=True)
    op.alter_column('groups', 'level',
               existing_type=sa.VARCHAR(length=40),
               nullable=True)
    op.alter_column('groups', 'course',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('subjects', 'short_name',
               existing_type=sa.VARCHAR(length=25),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('subjects', 'short_name',
               existing_type=sa.VARCHAR(length=25),
               nullable=False)
    op.alter_column('groups', 'course',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('groups', 'level',
               existing_type=sa.VARCHAR(length=40),
               nullable=False)
    op.alter_column('groups', 'department',
               existing_type=sa.VARCHAR(length=15),
               nullable=False)
    # ### end Alembic commands ###
