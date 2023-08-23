"""Database init

Revision ID: 78e3562692c6
Revises: 
Create Date: 2023-08-23 18:38:19.651004

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '78e3562692c6'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('city',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_city_id'), 'city', ['id'], unique=False)
    op.create_index(op.f('ix_city_name'), 'city', ['name'], unique=True)
    op.create_table('edge',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('from_city_id', sa.Integer(), nullable=True),
    sa.Column('to_city_id', sa.Integer(), nullable=True),
    sa.Column('distance', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['from_city_id'], ['city.id'], ),
    sa.ForeignKeyConstraint(['to_city_id'], ['city.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('from_city_id', 'to_city_id', name='_from_to_uc')
    )
    op.create_index(op.f('ix_edge_id'), 'edge', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_edge_id'), table_name='edge')
    op.drop_table('edge')
    op.drop_index(op.f('ix_city_name'), table_name='city')
    op.drop_index(op.f('ix_city_id'), table_name='city')
    op.drop_table('city')
    # ### end Alembic commands ###