from app import create_app, db
from app.models.models import User, Role, Department, AssetType, Asset, Permission
from dotenv import load_dotenv

load_dotenv()
app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {
        'db': db, 
        'User': User, 
        'Role': Role,
        'Department': Department,
        'AssetType': AssetType,
        'Asset': Asset,
        'Permission': Permission
    }

# Create the database tables
with app.app_context():
    db.create_all()
    # Create roles if they don't exist
    if Role.query.count() == 0:
        Role.insert_roles()
        print("Roles created successfully!")

if __name__ == '__main__':
    app.run(debug=True) 