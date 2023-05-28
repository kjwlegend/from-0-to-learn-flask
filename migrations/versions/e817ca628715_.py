"""empty message

Revision ID: e817ca628715
Revises: 6485fd8ae207
Create Date: 2023-05-28 19:35:08.959542

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e817ca628715'
down_revision = '6485fd8ae207'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.create_foreign_key(None, 'category', ['category_id'], ['id'])

    with op.batch_alter_table('tags', schema=None) as batch_op:
        batch_op.create_foreign_key(None, 'tag', ['tag_id'], ['id'])
        batch_op.create_foreign_key(None, 'post', ['post_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('tags', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')

    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')

    # ### end Alembic commands ###
