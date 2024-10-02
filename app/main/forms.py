from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    SubmitField,
    FormField,
    DecimalField,
    FieldList,
)


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
