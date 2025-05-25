import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from flask_bcrypt import Bcrypt
from app.models.models import db, User

login_manager = LoginManager()
csrf = CSRFProtect()
bcrypt = Bcrypt()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def create_app(test_config=None):
    app = Flask(__name__)
    
    # Configure the app
    if test_config is None:
        app.config.from_mapping(
            SECRET_KEY=os.environ.get('SECRET_KEY', 'dev'),
            SQLALCHEMY_DATABASE_URI=os.environ.get('DATABASE_URL', 'sqlite:///app.db'),
            SQLALCHEMY_TRACK_MODIFICATIONS=False
        )
    else:
        app.config.from_mapping(test_config)
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'
    csrf.init_app(app)
    bcrypt.init_app(app)
    
    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.main import main_bp
    from app.errors import errors_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(errors_bp)
    
    # Create database tables
    with app.app_context():
        db.create_all()
        
        # Create initial data if database is empty
        if User.query.count() == 0:
            from app.models.models import Department, AssetType
            
            # Create default admin user
            admin = User(username='admin', email='admin@example.com', is_admin=True)
            admin.set_password('admin123')
            db.session.add(admin)
            
            # Create default departments
            departments = [
                Department(name='IT', description='Information Technology Department'),
                Department(name='HR', description='Human Resources Department'),
                Department(name='Finance', description='Finance Department'),
                Department(name='Marketing', description='Marketing Department')
            ]
            db.session.add_all(departments)
            
            # Create default asset types
            asset_types = [
                AssetType(name='Laptop', description='Portable computers'),
                AssetType(name='Desktop', description='Desktop computers'),
                AssetType(name='Server', description='Server hardware'),
                AssetType(name='Printer', description='Printing devices'),
                AssetType(name='Network Equipment', description='Routers, switches, etc.')
            ]
            db.session.add_all(asset_types)
            
            db.session.commit()
    
    return app