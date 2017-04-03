"""empty message

Revision ID: 67c719301d23
Revises: b5b133138711
Create Date: 2017-04-03 18:31:31.207535

"""

# revision identifiers, used by Alembic.
revision = '67c719301d23'
down_revision = 'b5b133138711'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('bank',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('branch_name', sa.String(length=100), nullable=True),
    sa.Column('bank', sa.String(length=100), nullable=True),
    sa.Column('year', sa.Integer(), nullable=True),
    sa.Column('sector_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['sector_id'], ['sector.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('banks')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('banks',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('branch_name', sa.VARCHAR(length=100), autoincrement=False, nullable=True),
    sa.Column('bank', sa.VARCHAR(length=100), autoincrement=False, nullable=True),
    sa.Column('year', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('sector_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['sector_id'], [u'sector.id'], name=u'banks_sector_id_fkey'),
    sa.PrimaryKeyConstraint('id', name=u'banks_pkey')
    )
    op.drop_table('bank')
    ### end Alembic commands ###