import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from config import Config

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()
bcrypt = Bcrypt()
migrate = Migrate()

login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)
    bcrypt.init_app(app)
    
    # Register blueprints
    from app.routes.auth import auth as auth_blueprint
    from app.routes.main import main_bp as main_blueprint
    from app.errors import errors_bp
    
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(main_blueprint)
    app.register_blueprint(errors_bp)
    
    # Register error handlers
    from app.errors import register_error_handlers
    register_error_handlers(app)
    
    # Setup roles
    with app.app_context():
        db.create_all()
        
        # Create initial data if database is empty
        from app.models.models import User, Department, AssetType, Role
        
        if User.query.count() == 0:
            # Create default admin user
            admin = User(username='admin', email='admin@example.com', is_admin=True)
            admin.password = 'admin123'
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
            
            # Create default roles
            Role.insert_roles()
            
            db.session.commit()
    
    # Make Permission available in templates
    from app.models.models import Permission
    @app.context_processor
    def inject_permissions():
        return dict(Permission=Permission)
    
    return app