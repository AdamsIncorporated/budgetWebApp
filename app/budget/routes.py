from flask import Blueprint, render_template
import random

budget = Blueprint(
    "budget",
    __name__,
    template_folder="templates/budget",
    static_folder="static",
    url_prefix="/budget",
)

data = [
    "SALARIES WAGES CONTRACT LABOR",
    "TOTAL LABOR COST",
    "PHYSICIAN SERVICES",
    "Purchased Services subtotal",
    "Public Relations Subtotal",
    "PURCHASED SERVICES TOTAL",
    "SUPPLIES TOTAL",
    "Facility Services Subtotal",
    "Rent/Lease Subtotal",
    "Professional Development Subtotal",
    "OTHER GOODS AND SERVICES",
    "TOTAL OPERATING EXPENSE",
]

data = {header: [random.randint(100, 999) for _ in range(22)] for header in data}
fiscal_year = 2024


@budget.route("/budget-entry")
def home():
    return render_template("home.html", data=data, fiscal_year=fiscal_year)
