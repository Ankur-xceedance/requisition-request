"""empty message

Revision ID: 55f2a2db6ef5
Revises: 
Create Date: 2018-01-21 22:01:11.014966

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '55f2a2db6ef5'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('client',
    sa.Column('client_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('client_id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('product',
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.Column('product', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('product_id'),
    sa.UniqueConstraint('product')
    )
    op.create_table('request',
    sa.Column('request_id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=100), nullable=True),
    sa.Column('desc', sa.String(length=1000), nullable=True),
    sa.Column('target_date', sa.Date(), nullable=True),
    sa.Column('client_id', sa.Integer(), nullable=True),
    sa.Column('product_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['client_id'], ['client.client_id'], ),
    sa.ForeignKeyConstraint(['product_id'], ['product.product_id'], ),
    sa.PrimaryKeyConstraint('request_id'),
    sa.UniqueConstraint('title')
    )
    op.create_index(op.f('ix_request_target_date'), 'request', ['target_date'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_request_target_date'), table_name='request')
    op.drop_table('request')
    op.drop_table('product')
    op.drop_table('client')
    # ### end Alembic commands ###
