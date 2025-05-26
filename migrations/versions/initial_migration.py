"""Initial migration with RBAC

Revision ID: 1a2b3c4d5e6f
Revises: 
Create Date: 2023-06-15 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from datetime import datetime

# revision identifiers, used by Alembic.
revision = '1a2b3c4d5e6f'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Create roles table
    op.create_table('roles',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=64), nullable=True),
        sa.Column('default', sa.Boolean(), nullable=True),
        sa.Column('permissions', sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )
    op.create_index(op.f('ix_roles_default'), 'roles', ['default'], unique=False)
    
    # Create users table
    op.create_table('users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('username', sa.String(length=64), nullable=True),
        sa.Column('email', sa.String(length=120), nullable=True),
        sa.Column('password_hash', sa.String(length=128), nullable=True),
        sa.Column('role_id', sa.Integer(), nullable=True),
        sa.Column('is_admin', sa.Boolean(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('last_login', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)
    
    # Create departments table
    op.create_table('departments',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=64), nullable=True),
        sa.Column('manager', sa.String(length=64), nullable=True),
        sa.Column('location', sa.String(length=128), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )
    
    # Create asset_types table
    op.create_table('asset_types',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=64), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )
    
    # Create assets table
    op.create_table('assets',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('tag', sa.String(length=64), nullable=True),
        sa.Column('name', sa.String(length=64), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('purchase_date', sa.DateTime(), nullable=True),
        sa.Column('purchase_cost', sa.Float(), nullable=True),
        sa.Column('status', sa.String(length=20), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.Column('department_id', sa.Integer(), nullable=True),
        sa.Column('type_id', sa.Integer(), nullable=True),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['department_id'], ['departments.id'], ),
        sa.ForeignKeyConstraint(['type_id'], ['asset_types.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('tag')
    )
    
    # Insert default roles
    op.bulk_insert(
        sa.table('roles',
            sa.column('name', sa.String),
            sa.column('default', sa.Boolean),
            sa.column('permissions', sa.Integer)
        ),
        [
            {'name': 'User', 'default': True, 'permissions': 1},  # VIEW = 1
            {'name': 'Editor', 'default': False, 'permissions': 7},  # VIEW + EDIT + CREATE = 1 + 2 + 4 = 7
            {'name': 'Manager', 'default': False, 'permissions': 15},  # VIEW + EDIT + CREATE + DELETE = 1 + 2 + 4 + 8 = 15
            {'name': 'Administrator', 'default': False, 'permissions': 31},  # All permissions = 31
        ]
    )
    
    # Create admin user
    from werkzeug.security import generate_password_hash
    admin_role_id = op.get_bind().execute("SELECT id FROM roles WHERE name = 'Administrator'").fetchone()[0]
    
    op.bulk_insert(
        sa.table('users',
            sa.column('username', sa.String),
            sa.column('email', sa.String),
            sa.column('password_hash', sa.String),
            sa.column('role_id', sa.Integer),
            sa.column('is_admin', sa.Boolean),
            sa.column('is_active', sa.Boolean),
            sa.column('created_at', sa.DateTime)
        ),
        [
            {
                'username': 'admin',
                'email': 'admin@example.com',
                'password_hash': generate_password_hash('admin123'),
                'role_id': admin_role_id,
                'is_admin': True,
                'is_active': True,
                'created_at': datetime.utcnow()
            }
        ]
    )

def downgrade():
    op.drop_table('assets')
    op.drop_table('asset_types')
    op.drop_table('departments')
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
    op.drop_index(op.f('ix_roles_default'), table_name='roles')
    op.drop_table('roles') 