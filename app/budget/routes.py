from flask import Blueprint, render_template, request
from .forms import Budgets

budget = Blueprint(
    "budget",
    __name__,
    template_folder="templates/budget",
    static_folder="static",
    url_prefix="/budget",
)

@budget.route("/budget-entry/<int:fiscal_year>/<string:business_unit_id>", methods=['POST', 'GET'])
def home(fiscal_year: int, business_unit_id: str):
    form = Budgets()
    
    if request.method == 'GET':
        form.read(fiscal_year, business_unit_id)
    
    return render_template("home.html", form=form)
