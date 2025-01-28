"""create business category pages table instead of business category template

Revision ID: 949fb9f65373
Revises: 01d5123ecc30
Create Date: 2024-09-30 11:15:01.983645

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '949fb9f65373'
down_revision: Union[str, None] = '01d5123ecc30'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('business_category_pages',
    sa.Column('business_category_id', sa.Integer(), nullable=False),
    sa.Column('page_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['business_category_id'], ['business_categories.id'], ),
    sa.ForeignKeyConstraint(['page_id'], ['pages.id'], ),
    sa.PrimaryKeyConstraint('business_category_id', 'page_id')
    )
    op.drop_table('business_category_templates')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('business_category_templates',
    sa.Column('business_category_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('template_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['business_category_id'], ['business_categories.id'], name='business_category_templates_business_category_id_fkey'),
    sa.ForeignKeyConstraint(['template_id'], ['templates.id'], name='business_category_templates_template_id_fkey'),
    sa.PrimaryKeyConstraint('business_category_id', 'template_id', name='business_category_templates_pkey')
    )
    op.drop_table('business_category_pages')
    # ### end Alembic commands ###
