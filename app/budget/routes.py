from flask import Blueprint, render_template, request, flash, redirect, url_for
from .forms import Budgets
from repositories.models import ProposedBudget, UserBusinessUnit
from repositories.queries import queries
from app import db
from sqlalchemy import text
from flask_login import login_required, current_user

budget = Blueprint(
    "budget",
    __name__,
    template_folder="templates/budget",
    static_folder="static",
    url_prefix="/budget",
)


def sanitize(value: str, type_func):
    return type_func(value.replace(",", "")) if value else None


@budget.route(
    "/budget-entry/<int:fiscal_year>/<string:business_unit_id>", methods=["POST", "GET"]
)
@login_required
def home(fiscal_year: int, business_unit_id: str):
    # authenticate if the regular user has access to this page
    if not current_user.is_root_user:  # user is a normal user and not admin
        user_business_unit_ids = UserBusinessUnit.query.filter_by(
            user_id=current_user.id
        ).all()
        keys = [str(key.business_unit_id) for key in user_business_unit_ids]

        if not keys:  # no departments have been authorized for user
            return redirect(url_for("auth.not_an_authorized_user"))

        if (
            business_unit_id not in keys
        ):  # the wrong business unit has been assigned for user
            return redirect(url_for("auth.not_allowed"))

    form = Budgets()
    current_fiscal_year = f"FY{str(fiscal_year)[-2:]}"
    proposed_fiscal_year = f"FY{str(fiscal_year + 1)[-2:]}"
    form.business_unit_picklist.default = business_unit_id
    form.fiscal_year_picklist.default = proposed_fiscal_year

    if request.method == "GET":
        query = queries["budget"](
            proposed_fiscal_year, current_fiscal_year, business_unit_id
        )
        results = [row._mapping for row in db.session.execute(text(query)).fetchall()]
        form.process(data={"budgets": results})

    if request.method == "POST":
        if form.validate_on_submit():
            for budget in form.budgets:
                budget_data = {
                    "fiscal_year": sanitize(budget.FiscalYear.data, str),
                    "business_unit_id": sanitize(budget.BusinessUnitId.data, str),
                    "account_no": sanitize(budget.AccountNo.data, str),
                    "proposed_budget": sanitize(budget.ProposedBudget.data, float),
                    "business_case_name": sanitize(budget.BusinessCaseName.data, str),
                    "business_case_amount": sanitize(
                        budget.BusinessCaseAmount.data, float
                    ),
                    "comments": sanitize(budget.Comments.data, str),
                    "total_budget": sanitize(budget.TotalBudget.data, float),
                }

                budget_id = sanitize(budget.Id.data, int)
                row = (
                    ProposedBudget.query.get(budget_id)
                    if budget_id
                    else ProposedBudget()
                )

                for key, value in budget_data.items():
                    setattr(row, key, value)

                if not budget_id:
                    db.session.add(row)

            db.session.commit()

            # Reload data after submission
            query = queries["budget"](
                proposed_fiscal_year, current_fiscal_year, business_unit_id
            )
            results = [
                row._mapping for row in db.session.execute(text(query)).fetchall()
            ]
            form.process(data={"budgets": results})
            flash("Form submitted!", "success")
        else:
            flash("You have form errors!", "error")

    return render_template("home.html", form=form)
