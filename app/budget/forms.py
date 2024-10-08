from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    SubmitField,
    FormField,
    DecimalField,
    FieldList,
    IntegerField,
    HiddenField,
)
from app import db
from app.budget.models import (
    BusinessUnit,
    Budget as BudgetModel,
    Account,
    RAD,
    JournalEntry,
)


class Budget(FlaskForm):
    account_no = HiddenField()
    account = StringField()
    business_unit_id = HiddenField()
    business_unit = StringField()
    rad_description = StringField()
    two_year_prior_actual = DecimalField()
    two_year_prior_budget = DecimalField()
    two_year_prior_variance = DecimalField()
    one_year_prior_actual = DecimalField()
    one_year_prior_budget = DecimalField()
    one_year_prior_variance = DecimalField()
    one_year_prior_percent = DecimalField()
    actual_to_date = DecimalField()
    actual_budget = DecimalField()
    actual_variance = DecimalField()
    actual_percent = DecimalField()
    forecast = DecimalField()
    proposed_budget = DecimalField()
    yoy_change = DecimalField()
    comments = StringField()
    business_case_name = StringField()
    business_case_amount = DecimalField()
    total_budget = DecimalField()


class Budgets(FlaskForm):
    budget_items = FieldList(FormField(Budget), min_entries=1)
    fiscal_year = IntegerField()
    bussiness_unit_id = IntegerField()
    submit = SubmitField("Submit Budget")

    def read(self, fiscal_year: int, business_unit_id: int) -> any | None:
        budgets = BudgetModel.query.filter_by(
            fiscal_year=fiscal_year, business_unit_id=business_unit_id
        ).first()
