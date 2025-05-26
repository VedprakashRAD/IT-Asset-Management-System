from functools import wraps
from flask import abort, flash, redirect, url_for
from flask_login import current_user
from .models.models import Permission

def permission_required(permission):
    """
    Decorator that restricts access to users with specific permission
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.can(permission):
                flash('You do not have permission to access this page.', 'danger')
                return redirect(url_for('main.index'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def admin_required(f):
    """
    Decorator that restricts access to administrators
    """
    return permission_required(Permission.ADMIN)(f)

def role_required(role_name):
    """
    Decorator that restricts access to users with specific role
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.role or current_user.role.name != role_name:
                flash(f'You need to have {role_name} role to access this page.', 'danger')
                return redirect(url_for('main.index'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator 