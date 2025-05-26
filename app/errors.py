from flask import Blueprint, render_template

errors_bp = Blueprint('errors', __name__)

@errors_bp.app_errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@errors_bp.app_errorhandler(403)
def forbidden_error(error):
    return render_template('errors/403.html'), 403

@errors_bp.app_errorhandler(500)
def internal_error(error):
    return render_template('errors/500.html'), 500

def register_error_handlers(app):
    """Register error handlers with the Flask application."""
    app.register_error_handler(404, not_found_error)
    app.register_error_handler(403, forbidden_error)
    app.register_error_handler(500, internal_error) 