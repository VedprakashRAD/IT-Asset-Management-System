from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectField, FloatField, DateField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError, Optional
from app.models.models import User

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=50)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    password2 = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class DepartmentForm(FlaskForm):
    name = StringField('Department Name', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Description')
    submit = SubmitField('Submit')

class AssetTypeForm(FlaskForm):
    name = StringField('Asset Type Name', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Description')
    submit = SubmitField('Submit')

class AssetForm(FlaskForm):
    name = StringField('Asset Name', validators=[DataRequired(), Length(max=100)])
    serial_number = StringField('Serial Number', validators=[DataRequired(), Length(max=100)])
    purchase_date = DateField('Purchase Date', format='%Y-%m-%d', validators=[Optional()])
    purchase_cost = FloatField('Purchase Cost', validators=[Optional()])
    notes = TextAreaField('Notes')
    status = SelectField('Status', choices=[
        ('Available', 'Available'),
        ('Assigned', 'Assigned'),
        ('Maintenance', 'Maintenance'),
        ('Retired', 'Retired')
    ])
    department_id = SelectField('Department', coerce=int, validators=[DataRequired()])
    asset_type_id = SelectField('Asset Type', coerce=int, validators=[DataRequired()])
    assigned_to = SelectField('Assigned To', coerce=int, validators=[Optional()], default=None)
    submit = SubmitField('Submit')

class UserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=50)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    is_admin = BooleanField('Admin')
    submit = SubmitField('Submit') 