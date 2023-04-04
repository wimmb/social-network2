from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    EmailField,
    validators,
    PasswordField,
    BooleanField,
    SubmitField
)


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[validators.DataRequired(message="User name is required")])
    password = PasswordField("Password", validators=[
        validators.DataRequired(message="Password is required"),
        validators.Length(min=6, message="Min 6 length or password is required")
    ])
    remember = BooleanField("Remember")
    submit = SubmitField("Log In")


class RegisterForm(LoginForm):
    email = EmailField("Email", validators=[validators.DataRequired(message="Email is required"), validators.Email()])
    confirm_password = PasswordField("Confirm password", validators=[
        validators.DataRequired(message="Confirm password is required"),
        validators.EqualTo("password", message="Password should match")
    ])
    submit = SubmitField("Register")
