from app import create_app
from app.models.models import User, Permission

app = create_app()

with app.app_context():
    admin = User.query.filter_by(email='admin@example.com').first()
    print(f'Admin exists: {admin is not None}')
    if admin:
        print(f'Admin username: {admin.username}')
        print(f'Admin role: {admin.role.name if admin.role else None}')
        print(f'Admin permissions: {admin.role.permissions if admin.role else None}')
        print(f'Admin can view: {admin.can(Permission.VIEW)}')
        print(f'Admin is_admin flag: {admin.is_admin}') 