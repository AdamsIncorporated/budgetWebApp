from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    SubmitField,
    FormField,
    FieldList,
    HiddenField,
    SelectField
)
from repositories.queries import queries

# def get_fiscal_year_picklist():
#         query = queries['fetch_all_fiscal_years']
#         records = DatabaseManager().fetch_all(query)
#         data = [entry['FiscalYear'] for entry in records]
#         return data

# def get_business_unit_picklist():
#         query  = queries['fetch_all_business_units']
#         records = DatabaseManager().fetch_all(query)
#         data = [entry['BusinessUnitId'] for entry in records]
#         return data

# FISCAL_YEAR_PICKLIST_CHOICES = get_fiscal_year_picklist()
# BUSINESS_UNIT_PICKLIST_CHOICES = get_business_unit_picklist()

class Budget(FlaskForm):
    Id = HiddenField()
    AccountNo = HiddenField()
    Account = StringField(render_kw={'readonly': True})
    Actual = StringField(render_kw={'readonly': True})
    Budget = StringField(render_kw={'readonly': True})
    Variance = StringField(render_kw={'readonly': True})
    Percent = StringField(render_kw={'readonly': True})
    ForecastAmount = StringField(render_kw={'readonly': True})
    ProposedBudget = StringField(render_kw={'masknumber': True})
    BusinessCaseName = StringField()
    BusinessCaseAmount = StringField(render_kw={'masknumber': True})
    Comments = StringField()
    TotalBudget = StringField(render_kw={'masknumber': True})


class Budgets(FlaskForm):
    budgets = FieldList(FormField(Budget), min_entries=1)
    fiscal_year_picklist = SelectField()
    business_unit_picklist = SelectField()
    submit = SubmitField("Submit Budget")