import unittest
from app import create_app
from app.models.models import db, User, Department, AssetType, Asset
from datetime import datetime

class ModelsTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app({
            'TESTING': True,
            'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
            'WTF_CSRF_ENABLED': False
        })
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
        
    def test_user_model(self):
        # Create a user
        user = User(username='testuser', email='test@example.com')
        user.set_password('password')
        db.session.add(user)
        db.session.commit()
        
        # Test user retrieval
        retrieved_user = User.query.filter_by(username='testuser').first()
        self.assertIsNotNone(retrieved_user)
        self.assertEqual(retrieved_user.email, 'test@example.com')
        self.assertFalse(retrieved_user.is_admin)
        
        # Test password checking
        self.assertTrue(retrieved_user.check_password('password'))
        self.assertFalse(retrieved_user.check_password('wrongpassword'))
        
    def test_department_model(self):
        # Create a department
        department = Department(name='Test Department', description='Test Description')
        db.session.add(department)
        db.session.commit()
        
        # Test department retrieval
        retrieved_department = Department.query.filter_by(name='Test Department').first()
        self.assertIsNotNone(retrieved_department)
        self.assertEqual(retrieved_department.description, 'Test Description')
        
    def test_asset_type_model(self):
        # Create an asset type
        asset_type = AssetType(name='Test Type', description='Test Description')
        db.session.add(asset_type)
        db.session.commit()
        
        # Test asset type retrieval
        retrieved_asset_type = AssetType.query.filter_by(name='Test Type').first()
        self.assertIsNotNone(retrieved_asset_type)
        self.assertEqual(retrieved_asset_type.description, 'Test Description')
        
    def test_asset_model(self):
        # Create prerequisites
        user = User(username='testuser', email='test@example.com')
        department = Department(name='Test Department', description='Test Description')
        asset_type = AssetType(name='Test Type', description='Test Description')
        
        db.session.add_all([user, department, asset_type])
        db.session.commit()
        
        # Create an asset
        asset = Asset(
            name='Test Asset',
            serial_number='SN12345',
            purchase_date=datetime.now().date(),
            purchase_cost=1000.0,
            notes='Test Notes',
            status='Available',
            department_id=department.id,
            asset_type_id=asset_type.id,
            assigned_to=user.id
        )
        
        db.session.add(asset)
        db.session.commit()
        
        # Test asset retrieval
        retrieved_asset = Asset.query.filter_by(serial_number='SN12345').first()
        self.assertIsNotNone(retrieved_asset)
        self.assertEqual(retrieved_asset.name, 'Test Asset')
        self.assertEqual(retrieved_asset.purchase_cost, 1000.0)
        self.assertEqual(retrieved_asset.status, 'Available')
        self.assertEqual(retrieved_asset.department.name, 'Test Department')
        self.assertEqual(retrieved_asset.asset_type.name, 'Test Type')
        self.assertEqual(retrieved_asset.user.username, 'testuser')
        
if __name__ == '__main__':
    unittest.main() 