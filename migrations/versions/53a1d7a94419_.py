"""empty message

Revision ID: 53a1d7a94419
Revises: 
Create Date: 2023-05-24 22:59:50.125935

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '53a1d7a94419'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('category',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=20), nullable=True),
    sa.Column('icon', sa.String(length=50), nullable=True),
    sa.Column('parent_category_id', sa.Integer(), nullable=True),
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.Column('update_time', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['parent_category_id'], ['category.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('category')
    # ### end Alembic commands ###