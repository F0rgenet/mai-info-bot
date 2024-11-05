"""initial

Revision ID: f2972392367d
Revises: 
Create Date: 2024-11-05 19:00:17.136794

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f2972392367d'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('abbreviations',
    sa.Column('name', sa.String(length=30), nullable=False),
    sa.Column('short_name', sa.String(length=10), nullable=False),
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name'),
    sa.UniqueConstraint('short_name')
    )
    op.create_table('classrooms',
    sa.Column('name', sa.String(length=25), nullable=False),
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('groups',
    sa.Column('name', sa.String(length=15), nullable=False),
    sa.Column('department', sa.String(length=15), nullable=False),
    sa.Column('level', sa.String(length=40), nullable=False),
    sa.Column('course', sa.Integer(), nullable=False),
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('teachers',
    sa.Column('full_name', sa.String(length=50), nullable=False),
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('full_name')
    )
    op.create_table('types',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('short_name', sa.String(length=5), nullable=False),
    sa.Column('full_name', sa.String(length=25), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('full_name'),
    sa.UniqueConstraint('short_name')
    )
    op.create_table('subjects',
    sa.Column('name', sa.String(length=150), nullable=False),
    sa.Column('abbreviation_id', sa.Uuid(), nullable=True),
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.ForeignKeyConstraint(['abbreviation_id'], ['abbreviations.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('entries',
    sa.Column('start_datetime', sa.DateTime(), nullable=False),
    sa.Column('end_datetime', sa.DateTime(), nullable=False),
    sa.Column('subject_id', sa.Uuid(), nullable=False),
    sa.Column('type_id', sa.Uuid(), nullable=False),
    sa.Column('group_id', sa.Uuid(), nullable=True),
    sa.Column('classroom_id', sa.Uuid(), nullable=True),
    sa.Column('teacher_id', sa.Uuid(), nullable=True),
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.ForeignKeyConstraint(['classroom_id'], ['classrooms.id'], ),
    sa.ForeignKeyConstraint(['group_id'], ['groups.id'], ),
    sa.ForeignKeyConstraint(['subject_id'], ['subjects.id'], ),
    sa.ForeignKeyConstraint(['teacher_id'], ['teachers.id'], ),
    sa.ForeignKeyConstraint(['type_id'], ['types.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('entries')
    op.drop_table('subjects')
    op.drop_table('types')
    op.drop_table('teachers')
    op.drop_table('groups')
    op.drop_table('classrooms')
    op.drop_table('abbreviations')
    # ### end Alembic commands ###