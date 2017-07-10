"""gh usage with versions

Revision ID: b4fbc8e04c81
Revises: 2bd5f6d0c8b0
Create Date: 2016-09-27 12:51:04.889059

"""

# revision identifiers, used by Alembic.
revision = 'b4fbc8e04c81'
down_revision = '2bd5f6d0c8b0'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('component_gh_usage',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('version', sa.String(length=255), nullable=False),
    sa.Column('count', sa.Integer(), nullable=False),
    sa.Column('ecosystem_backend', postgresql.ENUM('none', 'npm', 'maven', 'pypi', 'rubygems', 'scm', 'crates', 'nuget', name='ecosystem_backend_enum', create_type=False), nullable=True),
    sa.Column('timestamp', sa.DateTime(), server_default=sa.text('LOCALTIMESTAMP'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('component_gh_usage')
    ### end Alembic commands ###
