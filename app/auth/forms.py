from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, ValidationError


class CustomEmailValidator:
    def __init__(self, message=None):
        if not message:
            message = "Email must end with centralhealth.net"
        self.message = message

    def __call__(self, form, field):
        if not field.data.endswith("@centralhealth.net"):
            raise ValidationError(self.message)


class LoginForm(FlaskForm):
    email = StringField(
        "Email",
        validators=[
            DataRequired(),
            Email(message="Invalid email address"),
            CustomEmailValidator(),
        ],
        render_kw={
            "placeholder": "first.last@centralhealth.net",
            "class": "mt-1 block w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-teal-500",
        },
    )

    password = PasswordField(
        "Password",
        validators=[DataRequired()],
        render_kw={
            "placeholder": "Enter your password",
            "class": "mt-1 block w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-teal-500",
        },
    )

    submit = SubmitField(
        "Login",
        render_kw={
            "class": "w-full bg-teal-600 text-white py-2 rounded-md hover:bg-teal-700 focus:outline-none focus:ring-2 focus:ring-teal-500 focus:ring-opacity-50"
        },
    )
