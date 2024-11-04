from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    SubmitField,
    DateTimeField,
    HiddenField,
    FieldList,
    FormField,
    BooleanField,
    SelectField,
    FloatField,
)
from wtforms.validators import DataRequired, Email, Length, ValidationError, NumberRange
from app import db
from repositories.queries import queries
from repositories.models import MasterEmail, User
from sqlalchemy import text


class UserBusinessUnit(FlaskForm):
    id = HiddenField()
    is_business_unit_selected = BooleanField(default=False)
    business_unit = StringField()
    business_unit_id = StringField()


class UserBusinessUnits(FlaskForm):
    user_id = HiddenField()
    email = StringField("Email")
    date_created = DateTimeField(
        "Date Created", format="%Y-%m-%d %H:%M:%S", default=db.func.current_timestamp()
    )
    user_business_units = FieldList(
        FormField(UserBusinessUnit),
        min_entries=1,
        validators=[DataRequired()],
    )
    submit = SubmitField("Submit")

    def validate_user_business_units(self, field):
        # Check if at least one business unit is selected
        if not any(
            unit.is_business_unit_selected.data for unit in self.user_business_units
        ):
            raise ValidationError("At least one business unit must be selected")


class MasterEmailForm(FlaskForm):
    id = HiddenField()
    email = SelectField("Email", validators=[DataRequired(), Email(), Length(max=120)])
    date_created = DateTimeField(
        "Date Created", format="%Y-%m-%d %H:%M:%S", default=db.func.current_timestamp()
    )
    user_business_units = FieldList(
        FormField(UserBusinessUnit),
        min_entries=1,
        validators=[DataRequired()],
    )
    submit = SubmitField("Submit")

    def __init__(self, *args, **kwargs):
        super(MasterEmailForm, self).__init__(*args, **kwargs)
        self.populate_email_choices()

    def populate_email_choices(self):
        emails = User.query.with_entities(User.email).filter_by(is_root_user=0).all()
        self.email.choices = [(email[0]) for email in emails]

    def validate_email(self, field):
        # Check if the email already exists in the User table
        existing_user = MasterEmail.query.filter_by(email=field.data).first()
        if existing_user:
            raise ValidationError("Email already exists, please use a different email")

    def validate_user_business_units(self, field):
        # Check if at least one business unit is selected
        if not any(
            unit.is_business_unit_selected.data for unit in self.user_business_units
        ):
            raise ValidationError("At least one business unit must be selected")


class MultiviewTemplate(FlaskForm):
    fiscal_year = SelectField("Fiscal Year", validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        super(MultiviewTemplate, self).__init__(*args, **kwargs)
        self.populate_fiscal_year_choices()

    def populate_fiscal_year_choices(self):
        query = text(queries["fetch_all_proposed_fiscal_years"])
        result = db.session.execute(query).fetchall()
        self.fiscal_year.choices = [(row[0]) for row in result]


class BudgetEntryForm(FlaskForm):
    id = HiddenField()
    display_order = StringField("Display Order")
    account_no = StringField("Account No")
    account = SelectField("Account", validators=[DataRequired()])
    rad = SelectField("RAD", choices=[("", "Select RAD")])
    forecast_multiplier = FloatField(
        "Forecast Multiplier",
        default=1.0,
        validators=[
            NumberRange(
                min=1,
                max=500,
                message="Length of forecast is bound between 1x and 500x!",
            )
        ],
    )
    forecast_comments = StringField(
        "Forecast Comments",
        validators=[
            Length(
                min=0,
                max=500,
                message="Only 500 charcter limit allowed for the forecast comments field!",
            )
        ],
    )
    is_rad = BooleanField("Should this Require a RAD?", default=0)

    def __init__(self, *args, **kwargs):
        super(BudgetEntryForm, self).__init__(*args, **kwargs)

        self.account.choices = self.get_account_choices()

    def get_account_choices(self):
        query = queries["fetch_accounts_for_budget_admin_view"]
        data = db.session.execute(text(query))

        return [(item[0]) for item in data]

    def validate(self, extra_validators=None):
        # Call the parent class's validate method with extra_validators
        if not super(BudgetEntryForm, self).validate(extra_validators=extra_validators):
            return False

        account_rad = f"{self.account.data} {self.rad.data}"
        query = queries["validate_budget_entry_admin_view_row"](account_rad)
        result = db.session.execute(text(query)).fetchone()

        if result:
            # Add the error message to the form's errors instead of raising an exception
            self.account.errors.append(
                "Account and RAD combination present within the budget entry admin view!"
            )
            return False

        return True


class BudgetEntryAdminViewForm(FlaskForm):
    budget_entries = FieldList(FormField(BudgetEntryForm), min_entries=1)
    submit = SubmitField("Save")
