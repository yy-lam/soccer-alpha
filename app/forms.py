from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Length, ValidationError
from app.models import User

# Set your classes here.


class RegisterForm(FlaskForm):
    username = StringField(
        'Username', validators=[DataRequired(), Length(min=5, max=25)]
    )
    email = StringField(
        'Email', validators=[DataRequired(), Length(min=5, max=40)]
    )
    password = PasswordField(
        'Password', validators=[DataRequired(), Length(min=5, max=40)]
    )
    confirm = PasswordField(
        'Repeat Password',
        [DataRequired(),
        EqualTo('password', message='Passwords must match')]
    )
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Username is Already Registered')

    def validate_email(self, email):
        pass


class LoginForm(FlaskForm):
    username = StringField('Username', [DataRequired()])
    password = PasswordField('Password', [DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Sign in')


class ForgotForm(FlaskForm):
    email = StringField(
        'Email', validators=[DataRequired(), Length(min=6, max=40)])



