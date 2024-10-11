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
from repositories.db_manager import DatabaseManager

def get_fiscal_year_picklist():
        query = queries['fetch_all_fiscal_years']
        records = DatabaseManager().fetch_all(query)
        data = [entry['FiscalYear'] for entry in records]
        return data

def get_business_unit_picklist():
        query  = queries['fetch_all_business_units']
        records = DatabaseManager().fetch_all(query)
        data = [entry['BusinessUnitId'] for entry in records]
        return data

FISCAL_YEAR_PICKLIST_CHOICES = get_fiscal_year_picklist()
BUSINESS_UNIT_PICKLIST_CHOICES = get_business_unit_picklist()

class Budget(FlaskForm):
    Id = HiddenField()
    AccountNo = HiddenField()
    Account = StringField(render_kw={'disabled': True})
    Actual = StringField(render_kw={'disabled': True})
    Budget = StringField(render_kw={'disabled': True})
    Variance = StringField(render_kw={'disabled': True})
    Percent = StringField(render_kw={'disabled': True})
    ForecastAmount = StringField(render_kw={'masknumber': True})
    ProposedBudget = StringField(render_kw={'masknumber': True})
    BusinessCaseName = StringField()
    BusinessCaseAmount = StringField(render_kw={'masknumber': True})
    Comments = StringField()
    TotalBudget = StringField(render_kw={'masknumber': True})


class Budgets(FlaskForm):
    budgets = FieldList(FormField(Budget), min_entries=1)
    fiscal_year_picklist = SelectField(choices=FISCAL_YEAR_PICKLIST_CHOICES)
    business_unit_picklist = SelectField(choices=BUSINESS_UNIT_PICKLIST_CHOICES)
    submit = SubmitField("Submit Budget")

    def read(self, fiscal_year: int, business_unit_id: int):
        current_fiscal_year = f"FY{str(fiscal_year)[-2:]}"
        proposed_fiscal_year = f"FY{str(fiscal_year + 1)[-2:]}"
        query = queries['budget'](proposed_fiscal_year, current_fiscal_year, business_unit_id)
        records = DatabaseManager().fetch_all(query)
        data = {'budgets': records}
        self.process(data=data)

    def write(self, fiscal_year: int, business_unit_id: int):
        pass