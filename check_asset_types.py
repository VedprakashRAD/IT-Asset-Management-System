from app import create_app, db
from app.models.models import AssetType, Asset

app = create_app()

with app.app_context():
    asset_types = AssetType.query.all()
    print(f"Number of asset types: {len(asset_types)}")
    
    for asset_type in asset_types:
        print(f"Asset Type: {asset_type.name}, ID: {asset_type.id}")
        print(f"  Description: {asset_type.description}")
        print(f"  Assets: {asset_type.assets.count()}")
        
    # Check Asset model
    assets = Asset.query.all()
    print(f"\nNumber of assets: {len(assets)}")
    
    for asset in assets:
        print(f"Asset: {asset.name}, ID: {asset.id}")
        print(f"  Type ID: {asset.type_id}")
        try:
            print(f"  Type: {asset.type.name if asset.type else 'None'}")
        except Exception as e:
            print(f"  Error accessing type: {str(e)}") 