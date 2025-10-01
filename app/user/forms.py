from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators

class SignupForm(FlaskForm):
    username = StringField("Username", [
        validators.DataRequired(),
        validators.Length(min=3, max=25)
    ])
    email = StringField("Email", [
        validators.DataRequired(),
        validators.Length(min=6, max=50)
    ])
    password = PasswordField("Password", [
        validators.DataRequired(),
        validators.Length(min=6) 
    ])


class LoginForm(FlaskForm):
    username = StringField("Username", [
        validators.DataRequired(),
        validators.Length(min=3, max=25)
    ])
    password = PasswordField("Password", [
        validators.DataRequired()
    ])
