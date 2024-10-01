from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    SubmitField,
    BooleanField,
    FormField,
    DecimalField,
    FieldList,
)
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flaskblog.models import User


class RegistrationForm(FlaskForm):
    username = StringField(
        "Username", validators=[DataRequired(), Length(min=2, max=20)]
    )
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField(
        "Confirm Password", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Sign Up")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(
                "That username is taken. Please choose a different one."
            )

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("That email is taken. Please choose a different one.")


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Login")


class Budget(FlaskForm):
    account = StringField()
    rad_description = StringField()
    account_code = StringField()
    one_year_prior_actual = DecimalField()
    one_year_prior_budget = DecimalField()
    one_year_prior_variance = DecimalField()
    one_year_prior_percent = DecimalField()
    two_year_prior_actual = DecimalField()
    two_year_prior_budget = DecimalField()
    two_year_prior_variance = DecimalField()
    actual_to_date = DecimalField()
    budget = DecimalField()
    variance = DecimalField()
    percent = DecimalField()
    forecast = DecimalField()
    proposed_budget = DecimalField()
    yoy_change = DecimalField()
    comments = StringField()
    business_case_name = StringField()
    business_case_amount = DecimalField()
    total_budget = DecimalField()


class Budgets(FlaskForm):
    budget_items = FieldList(FormField(Budget), min_entries=1)
    submit = SubmitField("Submit Budget")
