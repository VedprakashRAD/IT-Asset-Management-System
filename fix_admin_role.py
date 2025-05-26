from app import create_app, db
from app.models.models import User, Role, Permission

app = create_app()

with app.app_context():
    # First, make sure roles are created
    Role.insert_roles()
    
    # Get the admin role
    admin_role = Role.query.filter_by(name='Administrator').first()
    if not admin_role:
        print("Error: Administrator role not found!")
        exit(1)
    
    # Find admin user and set role
    admin = User.query.filter_by(email='admin@example.com').first()
    if not admin:
        print("Error: Admin user not found!")
        exit(1)
    
    # Set admin role
    admin.role = admin_role
    admin.is_admin = True
    db.session.commit()
    
    # Verify changes
    print(f"Admin user updated:")
    print(f"Username: {admin.username}")
    print(f"Role: {admin.role.name}")
    print(f"Permissions: {admin.role.permissions}")
    print(f"Can view: {admin.can(Permission.VIEW)}")
    print(f"Is admin flag: {admin.is_admin}")
    
    print("\nAll roles in the system:")
    roles = Role.query.all()
    for role in roles:
        print(f"Role: {role.name}, Permissions: {role.permissions}, Default: {role.default}") 