from functools import wraps
from flask import Blueprint, render_template, request, flash, redirect, url_for
from .forms import Budgets
from repositories.models import ProposedBudget, UserBusinessUnit
from repositories.queries import queries
from app import db
from sqlalchemy import text
from flask_login import login_required, current_user
from services.current_user_image import image_wrapper

budget = Blueprint(
    "budget",
    __name__,
    template_folder="templates/budget",
    static_folder="static",
    url_prefix="/budget",
)


def sanitize(value: str, type_func):
    return type_func(value.replace(",", "")) if value else None


def get_default_historical_fiscal_year():
    result = db.session.execute(
        text(queries["fetch_default_historical_fiscal_year"])
    ).all()
    value = result[0][0]
    return value


def get_default_proposed_fiscal_year():
    result = db.session.execute(
        text(queries["fetch_all_default_proposed_fiscal_year"])
    ).all()
    value = result[0][0]
    return value


def get_all_business_units():
    if (
        not current_user.is_root_user
    ):  # not admin so we query very specific business units
        query = text(
            queries["fetch_all_regular_user_business_unit_ids"](user_id=current_user.id)
        )
    else:
        query = text(queries["fetch_all_business_unit_ids"])

    data = db.session.execute(query).fetchall()

    return [(item[0], item[1]) for item in data]


def authorize_business_unit(f):
    @wraps(f)
    def decorated_function(business_unit_id, *args, **kwargs):
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

        return f(business_unit_id, *args, **kwargs)

    return decorated_function


@budget.route("/budget-entry/<string:business_unit_id>", methods=["POST", "GET"])
@login_required
@image_wrapper
@authorize_business_unit
def home(business_unit_id: str, image_file=None):
    form = Budgets()
    form.business_unit_picklist.choices = get_all_business_units()
    form.business_unit_picklist.default = business_unit_id

    if request.method == "GET":
        historical_fiscal_year = request.args.get(
            "historical_fiscal_year", default=get_default_historical_fiscal_year()
        )
        proposed_fiscal_year = request.args.get(
            "proposed_fiscal_year", default=get_default_proposed_fiscal_year()
        )
        form.historical_fiscal_year_picklist.default = historical_fiscal_year
        form.proposed_fiscal_year_picklist.default = proposed_fiscal_year
        data = queries["budget_entry_view"](
            historical_fiscal_year, proposed_fiscal_year, business_unit_id
        )
        form.process(data={"budgets": data})

    if request.method == "POST":
        historical_fiscal_year = form.historical_fiscal_year_picklist.data
        proposed_fiscal_year = form.proposed_fiscal_year_picklist.data

        if form.validate_on_submit():
            for budget in form.budgets:
                if budget.IsSubTotal.data == 0:
                    budget_data = {
                        "fiscal_year": sanitize(budget.FiscalYear.data, str),
                        "business_unit_id": sanitize(budget.BusinessUnitId.data, str),
                        "account_no": sanitize(budget.AccountNo.data, str),
                        "rad": sanitize(budget.RAD.data, str),
                        "proposed_budget": sanitize(budget.ProposedBudget.data, float),
                        "business_case_name": sanitize(
                            budget.BusinessCaseName.data, str
                        ),
                        "business_case_amount": sanitize(
                            budget.BusinessCaseAmount.data, float
                        ),
                        "comments": sanitize(budget.Comments.data, str),
                        "total_budget": sanitize(budget.TotalBudget.data, float),
                    }

                    proposed_budget_id = (
                        None
                        if budget.ProposedBudgetId.data == ""
                        else budget.ProposedBudgetId.data
                    )
                    row = (
                        ProposedBudget.query.get(proposed_budget_id)
                        if proposed_budget_id
                        else ProposedBudget()
                    )

                    for key, value in budget_data.items():
                        setattr(row, key, value)

                    if not proposed_budget_id:
                        db.session.add(row)

            db.session.commit()

            # Reload data after submission
            data = queries["budget_entry_view"](
                historical_fiscal_year, proposed_fiscal_year, business_unit_id
            )
            form.process(
                data={
                    "historical_fiscal_year_picklist": historical_fiscal_year,
                    "proposed_fiscal_year_picklist": proposed_fiscal_year,
                    "budgets": data,
                }
            )
            flash("Form submitted!", "success")
        else:
            flash("You have form errors!", "error")

    return render_template("home.html", form=form, image_file=image_file)
