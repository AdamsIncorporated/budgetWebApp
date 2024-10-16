from flask import Blueprint, render_template, request, flash
from .forms import Budgets
from .models import ProposedBudget
from repositories.queries import queries
from app import db
from sqlalchemy import text

budget = Blueprint(
    "budget",
    __name__,
    template_folder="templates/budget",
    static_folder="static",
    url_prefix="/budget",
)

def sanitize_currency(value: str) -> float | None:
    if value != "":
        return float(str(value).replace(',', ''))
    return None

def sanitize_str(value: str) -> str | None:
    if value != "":
        return value
    return None

def sanitize_int(value: str) -> int | None:
    if value != "":
        return int(value)
    return None

@budget.route(
    "/budget-entry/<int:fiscal_year>/<string:business_unit_id>", methods=["POST", "GET"]
)
def home(fiscal_year: int, business_unit_id: str):
    form = Budgets()
    current_fiscal_year = f"FY{str(fiscal_year)[-2:]}"
    proposed_fiscal_year = f"FY{str(fiscal_year + 1)[-2:]}"

    if request.method == "GET":
        query = queries['budget'](proposed_fiscal_year, current_fiscal_year, business_unit_id)
        rows = db.session.execute(text(query)).fetchall()
        results = [row._mapping for row in rows]
        data = {"budgets": results}
        form.process(data=data)
        
    if request.method == "POST":
        if form.validate_on_submit():
            # Commit data to db
            for budget in form.budgets:
                budget_id = sanitize_int(budget.Id.data)
                
                # Check if the row exists in the database
                if budget_id:
                    # Fetch the existing ProposedBudget row
                    row = ProposedBudget.query.get(budget_id)
                    if row:
                        # Update the existing row with new values, but keep the ID unchanged
                        row.fiscal_year = sanitize_str(budget.FiscalYear.data)
                        row.business_unit_id = sanitize_str(budget.BusinessUnitId.data)
                        row.account_no = sanitize_str(budget.AccountNo.data)
                        row.proposed_budget = sanitize_currency(budget.ProposedBudget.data)
                        row.business_case_name = sanitize_str(budget.BusinessCaseName.data)
                        row.business_case_amount = sanitize_currency(budget.BusinessCaseAmount.data)
                        row.comments = sanitize_str(budget.Comments.data)
                        row.total_budget = sanitize_currency(budget.TotalBudget.data)
                    else:
                        # If the row does not exist, create a new one
                        row = ProposedBudget(
                            fiscal_year=sanitize_str(budget.FiscalYear.data),
                            business_unit_id=sanitize_str(budget.BusinessUnitId.data),
                            account_no=sanitize_str(budget.AccountNo.data),
                            proposed_budget=sanitize_currency(budget.ProposedBudget.data),
                            business_case_name=sanitize_str(budget.BusinessCaseName.data),
                            business_case_amount=sanitize_currency(budget.BusinessCaseAmount.data),
                            comments=sanitize_str(budget.Comments.data),
                            total_budget=sanitize_currency(budget.TotalBudget.data)
                        )
                        db.session.add(row)
                else:
                    # If there is no ID, add a new row
                    row = ProposedBudget(
                        fiscal_year=sanitize_str(budget.FiscalYear.data),
                        business_unit_id=sanitize_str(budget.BusinessUnitId.data),
                        account_no=sanitize_str(budget.AccountNo.data),
                        proposed_budget=sanitize_currency(budget.ProposedBudget.data),
                        business_case_name=sanitize_str(budget.BusinessCaseName.data),
                        business_case_amount=sanitize_currency(budget.BusinessCaseAmount.data),
                        comments=sanitize_str(budget.Comments.data),
                        total_budget=sanitize_currency(budget.TotalBudget.data)
                    )
                    db.session.add(row)

            db.session.commit()

            # Success, so read the data again as sanity check    
            query = queries['budget'](proposed_fiscal_year, current_fiscal_year, business_unit_id)
            rows = db.session.execute(text(query)).fetchall()
            results = [row._mapping for row in rows]
            data = {"budgets": results}
            form.process(data=data)
            flash('Form submitted!', 'success')
        else:
            flash("You have form errors!", "error")

    return render_template("home.html", form=form)
