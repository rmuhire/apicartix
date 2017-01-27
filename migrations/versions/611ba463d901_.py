"""empty message

Revision ID: 611ba463d901
Revises: 7ef35c35ff93
Create Date: 2017-01-27 16:29:43.656673

"""

# revision identifiers, used by Alembic.
revision = '611ba463d901'
down_revision = '7ef35c35ff93'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('saving_group', sa.Column('uniq_id', sa.String(length=240), nullable=True))
    op.create_unique_constraint(None, 'saving_group', ['uniq_id'])
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'saving_group', type_='unique')
    op.drop_column('saving_group', 'uniq_id')
    ### end Alembic commands ###
