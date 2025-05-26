from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectField, FloatField, DateField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError, Optional
from app.models.models import User, Role

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=64)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    password2 = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already in use. Please choose a different one.')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already registered. Please use a different one.')

class UserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=64)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField('Password', validators=[Optional(), Length(min=8)])
    role = SelectField('Role', coerce=int)
    is_active = BooleanField('Active')
    submit = SubmitField('Save')
    
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name) for role in Role.query.order_by(Role.name).all()]
    
    def validate_username(self, username):
        if self.user_id is None or self.user_id == 0:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Username already in use. Please choose a different one.')
    
    def validate_email(self, email):
        if self.user_id is None or self.user_id == 0:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Email already registered. Please use a different one.')

class AssetForm(FlaskForm):
    tag = StringField('Asset Tag', validators=[DataRequired(), Length(max=64)])
    name = StringField('Name', validators=[DataRequired(), Length(max=64)])
    description = TextAreaField('Description')
    purchase_date = DateField('Purchase Date', validators=[Optional()], format='%Y-%m-%d')
    purchase_cost = FloatField('Purchase Cost', validators=[Optional()])
    status = SelectField('Status', choices=[('Active', 'Active'), ('Maintenance', 'Maintenance'), ('Retired', 'Retired')])
    notes = TextAreaField('Notes')
    department_id = SelectField('Department', coerce=int)
    asset_type_id = SelectField('Asset Type', coerce=int)
    submit = SubmitField('Save')

class DepartmentForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=64)])
    manager = StringField('Manager', validators=[Length(max=64)])
    location = StringField('Location', validators=[Length(max=128)])
    description = TextAreaField('Description')
    submit = SubmitField('Save')

class AssetTypeForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=64)])
    description = TextAreaField('Description')
    submit = SubmitField('Save') 