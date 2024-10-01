from flask import Blueprint, render_template, request, redirect, flash, url_for
from repositories.db_manager import get_db_connection
import random

main = Blueprint("main", __name__, template_folder="templates", static_folder="static")

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

data = {header: [random.randint(100, 999) for _ in range(20)] for header in data}
fiscal_year = 2024

@main.route("/")
@main.route("/budget-entry")
def home():
    return render_template("index.html", data=data, fiscal_year=fiscal_year)


@main.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        # Check if the email ends with 'centralhealth'
        if not email.endswith("@centralhealth.net"):
            flash("Email must end with @centralhealth.net", "error")
            return redirect(url_for("login"))

        dummy_user = "samuel.adams@centralhealth.net"
        dummy_password = "1234"
        # conn = get_db_connection()
        # user = conn.execute(
        #     "SELECT * FROM users WHERE email = ? AND password = ?", (email, password)
        # ).fetchone()
        # conn.close()

        # If user exists and credentials are correct
        if dummy_user:
            flash("Login successful!", "dashboard")
            return redirect(url_for("success_login"))  # redirect to a dashboard page
        else:
            flash("Invalid email or password", "error")
            return redirect(url_for("login"))

    return render_template("login.html")


@main.route("/success_login")
def success_login():
    return render_template("dashboard.html")
