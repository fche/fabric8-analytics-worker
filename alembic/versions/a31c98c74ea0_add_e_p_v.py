"""add_e_p_v

Revision ID: a31c98c74ea0
Revises: 79d88d57baa7
Create Date: 2016-08-01 11:42:44.000880

"""

# revision identifiers, used by Alembic.
revision = 'a31c98c74ea0'
down_revision = '79d88d57baa7'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    ecosystems = op.create_table('ecosystems',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.Column('_backend', sa.Enum('none', 'npm', 'maven', 'pypi', 'rubygems', 'scm', 'crates', 'nuget', name='ecosystem_backend_enum'), nullable=True),
    sa.Column('url', sa.String(length=255), nullable=True),
    sa.Column('fetch_url', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.bulk_insert(ecosystems,
        [
            {'id': 1, 'name': 'rubygems', '_backend': 'rubygems', 'url': 'https://rubygems.org/', 'fetch_url': 'https://rubygems.org/api/v1'},
            {'id': 2, 'name': 'npm', '_backend': 'npm', 'url': 'https://www.npmjs.com/', 'fetch_url': 'https://registry.npmjs.org/'},
            {'id': 3, 'name': 'maven', '_backend': 'maven', 'url': 'https://repo1.maven.org/maven2/', 'fetch_url': None},
            {'id': 4, 'name': 'pypi', '_backend': 'pypi', 'url': 'https://pypi.python.org/', 'fetch_url': 'https://pypi.python.org/pypi'},
            {'id': 5, 'name': 'go', '_backend': 'scm', 'url': None, 'fetch_url': None},
            {'id': 6, 'name': 'crates', '_backend': 'crates', 'url': 'https://crates.io/', 'fetch_url': None},
            {'id': 7, 'name': 'nuget', '_backend': 'nuget', 'url': 'https://nuget.org/', 'fetch_url': 'https://api.nuget.org/packages/'},
        ]
    )
    op.create_table('packages',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('ecosystem_id', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.ForeignKeyConstraint(['ecosystem_id'], ['ecosystems.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('ecosystem_id', 'name', name='ep_unique')
    )
    op.create_table('versions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('package_id', sa.Integer(), nullable=True),
    sa.Column('identifier', sa.String(length=255), nullable=True),
    sa.ForeignKeyConstraint(['package_id'], ['packages.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('package_id', 'identifier', name='pv_unique')
    )
    op.add_column('analyses', sa.Column('version_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'analyses', 'versions', ['version_id'], ['id'])
    op.drop_column('analyses', 'package')
    op.drop_column('analyses', 'ecosystem')
    op.drop_column('analyses', 'version')
    op.add_column('analysis_requests', sa.Column('version_id', sa.Integer(), nullable=True))
    op.drop_index('epv_index', table_name='analysis_requests')
    op.create_index('epv_index', 'analysis_requests', ['version_id'], unique=True, postgresql_where=sa.text('fulfilled_at IS NULL'))
    op.create_foreign_key(None, 'analysis_requests', 'versions', ['version_id'], ['id'])
    op.drop_column('analysis_requests', 'package')
    op.drop_column('analysis_requests', 'ecosystem')
    op.drop_column('analysis_requests', 'version')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('analysis_requests', sa.Column('version', sa.VARCHAR(length=255), autoincrement=False, nullable=True))
    op.add_column('analysis_requests', sa.Column('ecosystem', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('analysis_requests', sa.Column('package', sa.VARCHAR(length=255), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'analysis_requests', type_='foreignkey')
    op.drop_index('epv_index', table_name='analysis_requests')
    op.create_index('epv_index', 'analysis_requests', ['ecosystem', 'package', 'version'], unique=True)
    op.drop_column('analysis_requests', 'version_id')
    op.add_column('analyses', sa.Column('version', sa.VARCHAR(length=255), autoincrement=False, nullable=True))
    op.add_column('analyses', sa.Column('ecosystem', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('analyses', sa.Column('package', sa.VARCHAR(length=255), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'analyses', type_='foreignkey')
    op.drop_column('analyses', 'version_id')
    op.drop_table('versions')
    op.drop_table('packages')
    op.drop_table('ecosystems')
    ### end Alembic commands ###
