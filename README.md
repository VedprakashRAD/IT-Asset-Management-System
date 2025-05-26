# IT Asset Management System

A modern web application for managing IT assets with role-based access control.

## Features

- Modern UI with light/dark theme support
- Role-based access control (RBAC)
- Asset management
- Department management
- User management
- Responsive design

## Role-Based Access Control

The system implements a comprehensive role-based access control with the following roles:

1. **User** - Can view assets, departments, and asset types
2. **Editor** - Can view, create, and edit assets, departments, and asset types
3. **Manager** - Can view, create, edit, and delete assets, departments, and asset types
4. **Administrator** - Has full access to all features, including user management

### Permissions

The permission system is based on bitwise flags:

- VIEW = 1
- EDIT = 2
- CREATE = 4
- DELETE = 8
- ADMIN = 16

Each role has a combination of these permissions:

- User: VIEW (1)
- Editor: VIEW + EDIT + CREATE (7)
- Manager: VIEW + EDIT + CREATE + DELETE (15)
- Administrator: All permissions (31)

## Setup and Installation

1. Clone the repository
2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Initialize the database:
   ```
   flask db upgrade
   ```
5. Run the application:
   ```
   flask run
   ```

## Default Admin Account

The system creates a default administrator account:

- Username: admin
- Email: admin@example.com
- Password: admin123

**Important:** Change the default password after first login.

## Using the RBAC System

### For Developers

To protect routes with permission requirements:

```python
from app.decorators import permission_required, admin_required
from app.models.models import Permission

@app.route('/protected')
@login_required
@permission_required(Permission.EDIT)
def protected_route():
    # Only users with EDIT permission can access this
    return render_template('protected.html')

@app.route('/admin-only')
@login_required
@admin_required
def admin_route():
    # Only administrators can access this
    return render_template('admin.html')
```

### In Templates

Check permissions in templates:

```html
{% if current_user.can(Permission.EDIT) %}
    <a href="{{ url_for('main.edit_asset', id=asset.id) }}" class="btn btn-sm btn-outline-primary">
        <i class="bi bi-pencil"></i> Edit
    </a>
{% endif %}

{% if current_user.is_administrator() %}
    <a href="{{ url_for('main.admin') }}" class="nav-link">
        <i class="bi bi-gear"></i> Admin Panel
    </a>
{% endif %}
```

## License

MIT 