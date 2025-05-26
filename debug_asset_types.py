from app import create_app, db
from app.models.models import AssetType, Asset, User, Permission
from flask_login import login_user
from flask import url_for

app = create_app()

with app.app_context():
    # Get the admin user
    admin = User.query.filter_by(email='admin@example.com').first()
    print(f"Admin user: {admin.username}, Role: {admin.role.name if admin.role else None}")
    print(f"Admin can view: {admin.can(Permission.VIEW)}")
    
    # Check Asset model fields
    asset = Asset.query.first()
    if asset:
        print(f"Asset: {asset.name}")
        print(f"Asset type_id: {asset.type_id}")
        print(f"Asset department_id: {asset.department_id}")
    else:
        print("No assets found")
    
    # Check if there's a mismatch between Asset and AssetType
    print("\nChecking Asset model fields...")
    asset_columns = [column.name for column in Asset.__table__.columns]
    print(f"Asset columns: {asset_columns}")
    
    # Check the relationship between Asset and AssetType
    print("\nChecking relationship between Asset and AssetType...")
    
    # Create a test asset type
    test_type = AssetType(name="Test Type", description="For testing")
    db.session.add(test_type)
    db.session.flush()  # Get the ID without committing
    
    # Create a test asset with this type
    test_asset = Asset(
        name="Test Asset",
        type_id=test_type.id
    )
    db.session.add(test_asset)
    db.session.flush()
    
    try:
        print(f"Test asset type_id: {test_asset.type_id}")
        print(f"Test asset type: {test_asset.type}")
        print("Relationship works correctly")
    except Exception as e:
        print(f"Error in relationship: {str(e)}")
    
    # Rollback the test changes
    db.session.rollback()
    
    # Check the asset_types route
    print("\nChecking asset_types route...")
    with app.test_request_context():
        # Login as admin
        with app.test_client() as client:
            # Simulate login
            client.post('/login', data={
                'email': 'admin@example.com',
                'password': 'admin123'
            }, follow_redirects=True)
            
            # Try accessing asset_types
            response = client.get('/asset_types')
            print(f"Response status: {response.status_code}")
            if response.status_code != 200:
                print(f"Response: {response.data.decode('utf-8')}") 