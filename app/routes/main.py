from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from app.models.models import Asset, Department, AssetType, User, db
from app.forms.forms import AssetForm, DepartmentForm, AssetTypeForm, UserForm
from datetime import datetime
from functools import wraps

main_bp = Blueprint('main', __name__)

# Custom decorator for admin-only routes
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

@main_bp.route('/')
def index():
    return render_template('index.html', title='Home')

# Asset routes
@main_bp.route('/assets')
@login_required
def assets():
    assets = Asset.query.all()
    return render_template('assets/index.html', title='Assets', assets=assets)

@main_bp.route('/assets/new', methods=['GET', 'POST'])
@login_required
def new_asset():
    form = AssetForm()
    form.department_id.choices = [(d.id, d.name) for d in Department.query.order_by('name')]
    form.asset_type_id.choices = [(t.id, t.name) for t in AssetType.query.order_by('name')]
    form.assigned_to.choices = [(0, 'None')] + [(u.id, u.username) for u in User.query.order_by('username')]
    
    if form.validate_on_submit():
        asset = Asset(
            name=form.name.data,
            serial_number=form.serial_number.data,
            purchase_date=form.purchase_date.data,
            purchase_cost=form.purchase_cost.data,
            notes=form.notes.data,
            status=form.status.data,
            department_id=form.department_id.data,
            asset_type_id=form.asset_type_id.data
        )
        if form.assigned_to.data != 0:
            asset.assigned_to = form.assigned_to.data
            
        db.session.add(asset)
        db.session.commit()
        flash('Asset created successfully!', 'success')
        return redirect(url_for('main.assets'))
    
    return render_template('assets/form.html', title='New Asset', form=form)

@main_bp.route('/assets/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_asset(id):
    asset = Asset.query.get_or_404(id)
    form = AssetForm(obj=asset)
    form.department_id.choices = [(d.id, d.name) for d in Department.query.order_by('name')]
    form.asset_type_id.choices = [(t.id, t.name) for t in AssetType.query.order_by('name')]
    form.assigned_to.choices = [(0, 'None')] + [(u.id, u.username) for u in User.query.order_by('username')]
    
    if form.validate_on_submit():
        asset.name = form.name.data
        asset.serial_number = form.serial_number.data
        asset.purchase_date = form.purchase_date.data
        asset.purchase_cost = form.purchase_cost.data
        asset.notes = form.notes.data
        asset.status = form.status.data
        asset.department_id = form.department_id.data
        asset.asset_type_id = form.asset_type_id.data
        
        if form.assigned_to.data != 0:
            asset.assigned_to = form.assigned_to.data
        else:
            asset.assigned_to = None
            
        asset.updated_at = datetime.utcnow()
        db.session.commit()
        flash('Asset updated successfully!', 'success')
        return redirect(url_for('main.assets'))
    
    return render_template('assets/form.html', title='Edit Asset', form=form)

@main_bp.route('/assets/<int:id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_asset(id):
    asset = Asset.query.get_or_404(id)
    db.session.delete(asset)
    db.session.commit()
    flash('Asset deleted successfully!', 'success')
    return redirect(url_for('main.assets'))

# Department routes
@main_bp.route('/departments')
@login_required
def departments():
    departments = Department.query.all()
    return render_template('departments/index.html', title='Departments', departments=departments)

@main_bp.route('/departments/new', methods=['GET', 'POST'])
@login_required
@admin_required
def new_department():
    form = DepartmentForm()
    if form.validate_on_submit():
        department = Department(name=form.name.data, description=form.description.data)
        db.session.add(department)
        db.session.commit()
        flash('Department created successfully!', 'success')
        return redirect(url_for('main.departments'))
    
    return render_template('departments/form.html', title='New Department', form=form)

@main_bp.route('/departments/<int:id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_department(id):
    department = Department.query.get_or_404(id)
    form = DepartmentForm(obj=department)
    
    if form.validate_on_submit():
        department.name = form.name.data
        department.description = form.description.data
        db.session.commit()
        flash('Department updated successfully!', 'success')
        return redirect(url_for('main.departments'))
    
    return render_template('departments/form.html', title='Edit Department', form=form)

@main_bp.route('/departments/<int:id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_department(id):
    department = Department.query.get_or_404(id)
    if department.assets:
        flash('Cannot delete department with associated assets!', 'danger')
        return redirect(url_for('main.departments'))
    
    db.session.delete(department)
    db.session.commit()
    flash('Department deleted successfully!', 'success')
    return redirect(url_for('main.departments'))

# Asset Type routes
@main_bp.route('/asset_types')
@login_required
def asset_types():
    asset_types = AssetType.query.all()
    return render_template('asset_types/index.html', title='Asset Types', asset_types=asset_types)

@main_bp.route('/asset_types/new', methods=['GET', 'POST'])
@login_required
@admin_required
def new_asset_type():
    form = AssetTypeForm()
    if form.validate_on_submit():
        asset_type = AssetType(name=form.name.data, description=form.description.data)
        db.session.add(asset_type)
        db.session.commit()
        flash('Asset Type created successfully!', 'success')
        return redirect(url_for('main.asset_types'))
    
    return render_template('asset_types/form.html', title='New Asset Type', form=form)

@main_bp.route('/asset_types/<int:id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_asset_type(id):
    asset_type = AssetType.query.get_or_404(id)
    form = AssetTypeForm(obj=asset_type)
    
    if form.validate_on_submit():
        asset_type.name = form.name.data
        asset_type.description = form.description.data
        db.session.commit()
        flash('Asset Type updated successfully!', 'success')
        return redirect(url_for('main.asset_types'))
    
    return render_template('asset_types/form.html', title='Edit Asset Type', form=form)

@main_bp.route('/asset_types/<int:id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_asset_type(id):
    asset_type = AssetType.query.get_or_404(id)
    if asset_type.assets:
        flash('Cannot delete asset type with associated assets!', 'danger')
        return redirect(url_for('main.asset_types'))
    
    db.session.delete(asset_type)
    db.session.commit()
    flash('Asset Type deleted successfully!', 'success')
    return redirect(url_for('main.asset_types'))

# User management routes (admin only)
@main_bp.route('/users')
@login_required
@admin_required
def users():
    users = User.query.all()
    return render_template('users/index.html', title='Users', users=users)

@main_bp.route('/users/<int:id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_user(id):
    user = User.query.get_or_404(id)
    form = UserForm(obj=user)
    
    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data
        user.is_admin = form.is_admin.data
        db.session.commit()
        flash('User updated successfully!', 'success')
        return redirect(url_for('main.users'))
    
    return render_template('users/form.html', title='Edit User', form=form)

@main_bp.route('/users/<int:id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_user(id):
    if id == current_user.id:
        flash('You cannot delete your own account!', 'danger')
        return redirect(url_for('main.users'))
    
    user = User.query.get_or_404(id)
    if user.assigned_assets:
        flash('Cannot delete user with assigned assets!', 'danger')
        return redirect(url_for('main.users'))
    
    db.session.delete(user)
    db.session.commit()
    flash('User deleted successfully!', 'success')
    return redirect(url_for('main.users')) 