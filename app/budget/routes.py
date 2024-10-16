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
            form.write(fiscal_year, business_unit_id)
            form.read(fiscal_year, business_unit_id)
            flash('Form submitted!', 'success')
        else:
            flash("You have form errors!", "error")

    return render_template("home.html", form=form)
