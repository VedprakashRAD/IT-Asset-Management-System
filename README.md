# IT Asset Management System

A secure, comprehensive web application for managing IT assets across an organization, built with Python, Flask, and SQLite. This system was designed and implemented as part of the QAC020X328 Software Engineering and DevOps assignment.

## Project Overview

The IT Asset Management System is designed to address the challenges of tracking and managing IT assets within an organization. It provides a centralized platform where users can view their assigned assets, while administrators have extended capabilities to manage all assets, departments, asset types, and user accounts.

## Development Phases

### 1. Requirement Analysis
- Identified key stakeholders (IT managers, technicians, employees)
- Defined system requirements based on IT support role needs
- Created user stories for different roles (admin/regular users)
- Established scope limitations (four tables maximum, CRUD operations)
- Determined security requirements based on OWASP Top 10

### 2. System Design
- Designed a normalized database schema with four interconnected tables
- Created entity-relationship diagrams to visualize data relationships
- Established a modular application architecture (routes, models, forms, templates)
- Designed responsive user interfaces with Bootstrap 5
- Planned security measures at each application layer

### 3. Development
- Implemented database models using SQLAlchemy ORM
- Created form validation using Flask-WTF and WTForms
- Developed authentication system with Flask-Login and Bcrypt
- Implemented role-based access control for admin/regular users
- Built responsive templates with Bootstrap and Jinja2
- Added CRUD operations for assets, departments, and asset types

### 4. Testing
- Developed unit tests for models and routes
- Created integration tests for key workflows
- Implemented security testing against OWASP vulnerabilities
- Conducted manual usability testing
- Verified all requirements were met

### 5. Deployment
- Set up virtual environment for dependency management
- Created comprehensive requirements.txt for reproducibility
- Implemented configuration management
- Set up error handling and logging

## Features

- **User Authentication**: Secure login/registration with role-based access
- **Asset Management**: Full CRUD operations for IT assets
- **Department Organization**: Group assets by organizational departments
- **Asset Categorization**: Classify assets by type (laptop, desktop, etc.)
- **User Management**: Admin control over user accounts
- **Responsive Design**: Mobile-friendly interface using Bootstrap 5
- **Security**: Protection against OWASP Top 10 vulnerabilities

## Technical Implementation

### Database Architecture
The system uses SQLite with SQLAlchemy ORM and features four key tables:

1. **Users**: Stores user credentials and role information
   - Fields: id, username, email, password_hash, is_admin, created_at
   - Relationships: One-to-many with Assets (assigned_to)

2. **Assets**: Stores IT asset information
   - Fields: id, name, serial_number, purchase_date, purchase_cost, notes, status, created_at, updated_at
   - Foreign Keys: department_id, asset_type_id, assigned_to
   - Relationships: Many-to-one with Departments, AssetTypes, and Users

3. **Departments**: Organizes assets by organizational unit
   - Fields: id, name, description
   - Relationships: One-to-many with Assets

4. **AssetTypes**: Categorizes different types of assets
   - Fields: id, name, description
   - Relationships: One-to-many with Assets

### Application Structure
The application follows a modular structure to enhance maintainability:

- **Models**: Defines database schema and relationships using SQLAlchemy
- **Forms**: Handles input validation and CSRF protection using Flask-WTF
- **Routes**: Manages URL endpoints and HTTP request handling
- **Templates**: Renders dynamic HTML content using Jinja2
- **Static Files**: Contains CSS for custom styling

### Security Implementation

The system implements protection against the OWASP Top 10 web application security risks:

1. **Broken Access Control**: Role-based permissions using Flask-Login
2. **Cryptographic Failures**: Password hashing with Bcrypt
3. **Injection**: Parameterized queries via SQLAlchemy ORM
4. **Insecure Design**: Input validation on all forms
5. **Security Misconfiguration**: Proper error handling and configuration management
6. **Vulnerable Components**: Up-to-date dependencies with specific versions
7. **Identification and Authentication Failures**: Secure login system with Flask-Login
8. **Software and Data Integrity Failures**: CSRF protection with Flask-WTF
9. **Security Logging and Monitoring Failures**: Comprehensive error logging
10. **Server-Side Request Forgery**: Validated URLs and limited server-side requests

### DevOps Approach

The development followed modern DevOps practices:

- **Version Control**: Git/GitHub for source code management
- **Continuous Integration**: Automated testing setup
- **Dependency Management**: Virtual environment with requirements.txt
- **Configuration Management**: Environment-specific configurations
- **Testing Automation**: Pytest for automated testing

## Technologies Used

- **Backend**: Python 3.x, Flask 2.2.5
- **Database**: SQLite with SQLAlchemy 3.0.5
- **Authentication**: Flask-Login 0.6.2, Flask-Bcrypt 1.0.1
- **Form Handling**: Flask-WTF 1.1.1, WTForms 3.0.1
- **Frontend**: Bootstrap 5, HTML5, CSS3, JavaScript
- **Icons**: Bootstrap Icons
- **Testing**: Pytest 7.3.1

## Installation

1. Clone the repository:
```
git clone <repository-url>
cd it-asset-management
```

2. Create a virtual environment:
```
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```
pip install -r requirements.txt
```

4. Run the application:
```
python run.py
```

5. Access the application at http://localhost:5000

## Default Credentials

- **Admin User**:
  - Username: admin
  - Password: admin123

## Project Structure

```
it-asset-management/
├── app/
│   ├── models/
│   │   ├── __init__.py
│   │   └── models.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   └── main.py
│   ├── forms/
│   │   ├── __init__.py
│   │   └── forms.py
│   ├── static/
│   │   └── css/
│   │       └── style.css
│   ├── templates/
│   │   ├── auth/
│   │   │   ├── login.html
│   │   │   └── register.html
│   │   ├── assets/
│   │   │   ├── index.html
│   │   │   └── form.html
│   │   ├── departments/
│   │   │   ├── index.html
│   │   │   └── form.html
│   │   ├── asset_types/
│   │   │   ├── index.html
│   │   │   └── form.html
│   │   ├── users/
│   │   │   ├── index.html
│   │   │   └── form.html
│   │   ├── errors/
│   │   │   ├── 403.html
│   │   │   ├── 404.html
│   │   │   └── 500.html
│   │   ├── base.html
│   │   └── index.html
│   ├── __init__.py
│   └── errors.py
├── tests/
│   ├── __init__.py
│   ├── test_models.py
│   └── test_auth.py
├── requirements.txt
├── run.py
└── README.md
```

## Challenges and Solutions

During development, several challenges were encountered and resolved:

1. **Dependency Management**: 
   - Challenge: Initial Flask installation issues in the base environment
   - Solution: Created a dedicated virtual environment and specified compatible package versions

2. **Werkzeug Compatibility**: 
   - Challenge: The `url_parse` function was not available in newer Werkzeug versions
   - Solution: Modified the URL validation logic to use string methods instead

3. **Database Relationships**: 
   - Challenge: Managing complex relationships between users, assets, departments, and asset types
   - Solution: Leveraged SQLAlchemy's relationship features with appropriate backref configurations

4. **Security Implementation**: 
   - Challenge: Addressing OWASP Top 10 vulnerabilities comprehensively
   - Solution: Implemented specific security measures for each vulnerability type

## Future Enhancements

Potential improvements for future versions:

1. **Asset History Tracking**: Maintain a log of all changes to assets
2. **API Implementation**: Create a RESTful API for integration with other systems
3. **Advanced Reporting**: Generate customizable reports and analytics
4. **File Attachments**: Allow file uploads for asset documentation
5. **Multi-factor Authentication**: Enhance security with 2FA
6. **Email Notifications**: Alert users about asset assignments and changes

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Flask documentation and community
- Bootstrap team for the responsive design framework
- QAC020X328 course instructors for guidance on DevOps practices 