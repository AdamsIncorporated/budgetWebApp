from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    SubmitField,
    FormField,
    FieldList,
    HiddenField,
    SelectField
)
from wtforms.validators import Optional
from repositories.queries import queries
from app import db
from sqlalchemy import text
from app.dashboard.models import BusinessUnit


def get_fiscal_year_picklist():
        query = queries['fetch_all_fiscal_years']
        data = db.session.execute(text(query))
        
        return [(item[0]) for item in data]

def get_business_unit_picklist():
        query  = queries['fetch_all_business_units']
        data = db.session.execute(text(query))
        
        return [(item[0], item[1]) for item in data]

FISCAL_YEAR_PICKLIST_CHOICES = get_fiscal_year_picklist()
BUSINESS_UNIT_PICKLIST_CHOICES = get_business_unit_picklist()

class Budget(FlaskForm):
    Id = HiddenField()
    FiscalYear = HiddenField()
    BusinessUnitId = HiddenField()
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
    fiscal_year_picklist = SelectField(validators=[Optional()], choices=FISCAL_YEAR_PICKLIST_CHOICES)
    business_unit_picklist = SelectField(validators=[Optional()], choices=BUSINESS_UNIT_PICKLIST_CHOICES)
    submit = SubmitField("Submit Budget")
    
    def __init__(self, *args, **kwargs):
        super(Budgets, self).__init__(*args, **kwargs)
        business_units = (
            BusinessUnit.query.with_entities(
                BusinessUnit.id, BusinessUnit.business_unit
            )
            .distinct()
            .all()
        )
        self.business_unit_picklist.choices = [
            (bu.id, bu.business_unit) for bu in business_units
        ]