from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, FloatField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError, Optional
from .models import User

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=25)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    is_owner = BooleanField('Are you an owner?')
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already exists.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already registered.')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class TurfForm(FlaskForm):
    name = StringField('Turf Name', validators=[DataRequired(), Length(max=120)])
    city = StringField('City', validators=[Optional(), Length(max=80)])
    address = StringField('Address', validators=[Optional(), Length(max=200)])
    price_per_hour = FloatField('Price per Hour', validators=[DataRequired()], default=500.0)
    description = TextAreaField('Description', validators=[Optional()])
    image = FileField('Turf Image', validators=[FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Images only!')])
    submit = SubmitField('Save Turf')

class SlotForm(FlaskForm):
    date = StringField('Date', validators=[DataRequired()])
    start_time = StringField('Start Time', validators=[DataRequired()])
    end_time = StringField('End Time', validators=[DataRequired()])
    submit = SubmitField('Add Slot')