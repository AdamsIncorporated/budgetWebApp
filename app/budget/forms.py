from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    SubmitField,
    FormField,
    FieldList,
    HiddenField,
    SelectField,
    IntegerField,
)
from wtforms.validators import Optional
from repositories.queries import queries
from app import db
from sqlalchemy import text
from wtforms.validators import Length


def get_historical_fiscal_year_picklist():
    query = queries["fetch_all_historical_fiscal_years"]
    data = db.session.execute(text(query))

    return [(item[0]) for item in data]


def get_proposed_fiscal_year_picklist():
    query = queries["fetch_all_proposed_fiscal_years"]
    data = db.session.execute(text(query))

    return [(item[0]) for item in data]


HISTORICAL_FISCAL_YEAR_PICKLIST_CHOICES = get_historical_fiscal_year_picklist()
PROPOSED_FISCAL_YEAR_PICKLIST_CHOICES = get_proposed_fiscal_year_picklist()


class Budget(FlaskForm):
    ProposedBudgetId = HiddenField()
    FiscalYear = HiddenField()
    BusinessUnitId = HiddenField()
    AccountNo = HiddenField()
    Account = HiddenField()
    RAD = HiddenField()
    ActualsTotal = HiddenField()
    BudgetsTotal = HiddenField()
    Variance = HiddenField()
    ForecastAmount = HiddenField()
    ProposedBudget = StringField(render_kw={"masknumber": True})
    BusinessCaseName = StringField()
    BusinessCaseAmount = StringField(render_kw={"masknumber": True})
    Comments = StringField()
    TotalBudget = StringField(render_kw={"masknumber": True})
    IsSubTotal = IntegerField(default=0)

    @staticmethod
    def __sanitize_float(value: str) -> str | None:
        if value is "":
            return float(0)
        else:
            return float(value.replace(",", ""))

    @staticmethod
    def __sanitize_str(value: str) -> str | None:
        if value is "":
            return None
        else:
            return value

    def serialize_data(self) -> dict:
        budget_data = {
            "fiscal_year": self.__sanitize_str(self.FiscalYear.data),
            "business_unit_id": self.__sanitize_str(self.BusinessUnitId.data),
            "account_no": self.__sanitize_str(self.AccountNo.data),
            "rad": self.__sanitize_str(self.RAD.data),
            "proposed_budget": self.__sanitize_float(self.ProposedBudget.data),
            "business_case_name": self.BusinessCaseName.data,
            "business_case_amount": self.__sanitize_float(self.BusinessCaseAmount.data),
            "comments": self.__sanitize_str(self.Comments.data),
        }
        budget_data["total_budget"] = (
            budget_data["proposed_budget"] + budget_data["business_case_amount"]
        )

        return budget_data


class Budgets(FlaskForm):
    budgets = FieldList(FormField(Budget), min_entries=1)
    historical_fiscal_year_picklist = SelectField(
        validators=[Optional()], choices=HISTORICAL_FISCAL_YEAR_PICKLIST_CHOICES
    )
    proposed_fiscal_year_picklist = SelectField(
        validators=[Optional()], choices=PROPOSED_FISCAL_YEAR_PICKLIST_CHOICES
    )
    business_unit_picklist = SelectField(validators=[Optional()])
    submit = SubmitField("Submit Budget")
