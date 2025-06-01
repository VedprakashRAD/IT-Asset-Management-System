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

## Project Overview and Development Process

The IT Asset Management System is a comprehensive web application designed and developed for the QAC020X328 Software Engineering and DevOps assignment. The project demonstrates the application of modern software engineering principles, DevOps practices, and security measures in creating a real-world IT management solution.

### Development Process in Detail

1. **Requirement Analysis Phase**
   We began by carefully analyzing the assignment requirements, which specified developing a secure IT asset management system with a maximum of four database tables, CRUD operations, and protection against OWASP Top 10 vulnerabilities. We identified key stakeholders (IT managers, technicians, and regular employees) and created user stories to understand the needs of different user roles. This phase was crucial for establishing clear scope boundaries and security requirements.

2. **System Design Phase**
   During this phase, we designed a normalized database schema with four interconnected tables (Users, Assets, Departments, and AssetTypes) to efficiently organize the data. We created entity-relationship diagrams to visualize the relationships between these tables. The application architecture was designed to be modular, separating concerns into routes, models, forms, and templates, which promotes maintainability and scalability. We also planned responsive user interfaces using Bootstrap 5 and mapped out security measures for each application layer.

3. **Development Phase**
   The development began with setting up the Flask framework and implementing the database models using SQLAlchemy ORM. We created form validation with Flask-WTF and WTForms to ensure data integrity. The authentication system was developed using Flask-Login and Bcrypt for secure password hashing. Role-based access control was implemented to differentiate between regular users and administrators. Responsive templates were built using Bootstrap and Jinja2, and CRUD operations were implemented for assets, departments, and asset types.

4. **Testing Phase**
   Comprehensive testing was a key part of our development process. We developed unit tests for models and routes using pytest, created integration tests for key workflows, and implemented security testing against OWASP vulnerabilities. Manual usability testing was conducted to ensure a positive user experience. All requirements were systematically verified to ensure the application met the assignment specifications.

5. **Deployment Phase**
   To ensure reproducibility and ease of deployment, we set up a virtual environment for dependency management and created a comprehensive requirements.txt file with specific versions. We implemented configuration management to support different environments (development, testing, production) and set up error handling and logging for operational stability.

### Technical Challenges and Solutions

During the development process, we encountered several technical challenges:

1. **Dependency Management Challenge**
   When initiating the project, we encountered issues with Flask installations in the root Python environment. The ModuleNotFoundError: No module named 'flask' error issue stopped the application from running. We resolved this by creating a separate virtual environment with python -m venv venv and installing precise versions of all the dependencies. This approach of having separate environments is a DevOps best practice that guarantees uniformity across various development and deployment environments.

2. **Werkzeug Compatibility Issue**
  We had a compatibility problem with more recent versions of Werkzeug. The exception "ImportError: cannot import name 'url_parse' from 'werkzeug.urls'" was caused because the url_parse function had either been relocated or renamed in the version that we were utilizing. Instead of downgrading Werkzeug (which would bring additional compatibility problems), we changed our URL validation code to make use of more straightforward string methods to detect external URLs. This illustrated problem-solving and flexibility under dependency issues.

3. **Database Relationship Complexity**
   Managing the relationships between users, assets, departments, and asset types required careful consideration. We leveraged SQLAlchemy's relationship features with appropriate backref configurations to ensure data integrity and efficient querying. For example, the relationship between assets and users needed to handle both assignment and creation relationships while preventing circular dependencies.

4. **Comprehensive Security Implementation**
   Addressing all OWASP Top 10 vulnerabilities required a multi-layered approach. We implemented specific security measures for each vulnerability type, including role-based permissions with Flask-Login for broken access control, password hashing with Bcrypt for cryptographic failures, parameterized queries via SQLAlchemy ORM for injection protection, and CSRF protection with Flask-WTF for data integrity. This comprehensive approach demonstrates security by design principles.

### Key Technical Implementation Details

1. **Database Architecture**
   The SQLite database with SQLAlchemy ORM features four interconnected tables:
   - Users table stores credentials and role information with fields for id, username, email, password_hash, is_admin, and created_at.
   - Assets table contains IT asset details with fields for id, name, serial_number, purchase_date, purchase_cost, notes, status, created_at, and updated_at, plus foreign keys to departments, asset types, and assigned users.
   - Departments table organizes assets by organizational unit with fields for id, name, and description.
   - AssetTypes table categorizes assets with fields for id, name, and description.

2. **Authentication System**
   The authentication system uses Flask-Login for session management and Bcrypt for secure password hashing. When a user registers, their password is hashed using Bcrypt before storage. During login, the entered password is hashed and compared with the stored hash. The system also implements role-based access control, where certain routes and actions are restricted to users with admin privileges.

3. **Form Validation**
   All forms of input utilize Flask-WTF and WTForms for CSRF protection and validation. As an example, the asset creation form validates that necessary fields such as name and serial number are entered, that serial numbers are unique, and that dates and costs are properly formatted. This keeps bad data out of the system and helps prevent cross-site request forgery attacks.


4. **Responsive Interface**
  The user interface is developed on Bootstrap 5, thus it is mobile-responsive and runs on different devices. The templates use Jinja2 for dynamic content rendering, with conditional logic to show different options based on user roles. For instance, delete buttons are only shown to administrators, while regular users can only see and edit their assigned assets.

5. **Theme Management**
   The application implements a modern light/dark theme system with automatic detection of system preferences. The theme system uses CSS variables for consistent styling across the application and JavaScript for theme toggling and persistence. The UI adapts seamlessly between themes, ensuring proper contrast and readability in both modes.

6. **Table Enhancements**
   Tables throughout the application feature client-side sorting, filtering, and responsive behavior. The custom JavaScript provides interactive data manipulation without requiring page reloads, improving the user experience. Special care was taken to ensure tables render correctly in both light and dark themes.

## OWASP Top 10 Security Implementation

Our application addresses all relevant OWASP Top 10 vulnerabilities through careful design and implementation:

1. **A01:2021 - Broken Access Control**
   - Custom permission decorators enforce role-based access control
   - Route protection ensures users can only access authorized resources
   - UI elements dynamically adapt to user permissions
   - Session management with Flask-Login prevents unauthorized access

2. **A02:2021 - Cryptographic Failures**
   - Passwords are hashed using Bcrypt with appropriate salt
   - No sensitive data is stored in plaintext
   - HTTPS is recommended for production deployment

3. **A03:2021 - Injection**
   - SQLAlchemy ORM provides parameterized queries to prevent SQL injection
   - Input validation through WTForms sanitizes user input
   - Template engine (Jinja2) automatically escapes output to prevent XSS

4. **A04:2021 - Insecure Design**
   - Principle of least privilege applied through RBAC
   - Secure by default approach with explicit permission grants
   - Consistent error handling prevents information leakage

5. **A05:2021 - Security Misconfiguration**
   - Environment-specific configuration management
   - Detailed error messages only shown in development mode
   - Proper HTTP security headers implemented

6. **A06:2021 - Vulnerable and Outdated Components**
   - Specific dependency versions pinned in requirements.txt
   - Virtual environment isolation prevents system-wide conflicts
   - Regular updates can be managed through dependency tracking

7. **A07:2021 - Identification and Authentication Failures**
   - Strong password policies enforced through form validation
   - Account lockout functionality can be implemented
   - Session management with proper timeout and invalidation

8. **A08:2021 - Software and Data Integrity Failures**
   - CSRF protection on all forms prevents request forgery
   - Integrity checks on data modifications
   - Validation of all input data before processing

9. **A09:2021 - Security Logging and Monitoring Failures**
   - Comprehensive logging of authentication events
   - Audit trail for sensitive operations
   - Error logging for troubleshooting and security analysis

10. **A10:2021 - Server-Side Request Forgery**
    - Validation of URLs and external resources
    - Restricted network access from application server
    - Whitelisting approach for external resources

## DevOps Practices Implemented

The project incorporates several DevOps practices to ensure quality, consistency, and maintainability:

1. **Version Control**
   - Git repository with meaningful commit messages
   - Branch-based development workflow
   - Feature branches for isolated development

2. **Dependency Management**
   - Virtual environment isolation
   - Pinned dependency versions in requirements.txt
   - Clear documentation of setup process

3. **Configuration Management**
   - Environment-specific configuration
   - Separation of code and configuration
   - Use of environment variables for sensitive settings

4. **Continuous Integration**
   - Automated testing with pytest
   - Linting and code quality checks
   - Consistent development environment

5. **Deployment Automation**
   - Documented deployment process
   - Reproducible environment setup
   - Database migration management with Flask-Migrate

## Future Enhancements

While the current implementation meets all requirements, several enhancements could be considered for future versions:

1. **Advanced Asset Tracking**
   - QR code generation for physical asset tagging
   - Asset lifecycle management
   - Maintenance scheduling and history

2. **Reporting and Analytics**
   - Dashboard with key metrics and visualizations
   - Export functionality for reports
   - Custom report builder

3. **Integration Capabilities**
   - API endpoints for integration with other systems
   - Import/export functionality for bulk operations
   - Webhook support for event notifications

4. **Enhanced Security**
   - Two-factor authentication
   - OAuth integration for single sign-on
   - Advanced audit logging

5. **Performance Optimization**
   - Database query optimization
   - Caching strategies
   - Asynchronous processing for time-consuming operations

The IT Asset Management System demonstrates the successful application of software engineering principles, DevOps practices, and security measures to create a practical, secure, and maintainable web application. The project showcases skills in Python, Flask, database design, security implementation, and responsive web development, all within the context of modern DevOps methodologies.

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

## Conclusion

This IT Asset Management System project demonstrates how modern web development techniques, security best practices, and DevOps methodologies can be combined to create a robust application that meets real-world business needs. The implementation satisfies all requirements of the QAC020X328 Software Engineering and DevOps assignment while providing a practical solution for IT asset tracking and management.

TThe modular architecture of the project guarantees extensibility and maintainability, and the extensive security provisions guard against standard vulnerabilities. The permission system based on role-based access ensures fine-grained management of permissions, enabling the organizations to enforce the principle of least privilege effectively.

Following the DevOps culture throughout the development cycle, we have developed a solution that is easily deployable, manageable, and extendable. The documentation provided in this README offers clear guidance for developers who wish to understand, use, or extend the system.

## License

MIT 
