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
from wtforms.validators import DataRequired, Email, Length, ValidationError
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
    display_order = StringField("Display Order", validators=[DataRequired()])
    account_no = StringField("Account No", validators=[DataRequired()])
    account = SelectField("Account", validators=[DataRequired()])
    rad = SelectField("RAD")
    forecast_multiplier = FloatField("Forecast Multiplier")
    forecast_comments = StringField("Forecast Comments")

    def __init__(self, *args, **kwargs):
        super(BudgetEntryForm, self).__init__(*args, **kwargs)

        self.account.choices = self.get_account_choices()
        self.rad.choices = self.get_rad_choices()

    def get_account_choices(self):
        query = queries["fetch_all_accounts"]
        data = db.session.execute(text(query))

        return [(item[0]) for item in data]

    def get_rad_choices(self):
        query = queries["fetch_all_rads"]
        data = db.session.execute(text(query))

        return [(item[0]) for item in data]


class BudgetEntryAdminViewForm(FlaskForm):
    budget_entries = FieldList(FormField(BudgetEntryForm), min_entries=1)
    submit = SubmitField("Submit")
