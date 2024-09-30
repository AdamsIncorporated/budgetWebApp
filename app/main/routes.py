from flask import Blueprint, render_template, request, redirect, flash, url_for
from repositories.db_manager import get_db_connection

main = Blueprint("main", __name__, template_folder="templates", static_folder="static")


@main.route("/")
@main.route("/budget-entry")
def home():
    return render_template("index.html")


@main.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        # Check if the email ends with 'centralhealth'
        if not email.endswith("@centralhealth.net"):
            flash("Email must end with @centralhealth.net", "error")
            return redirect(url_for("login"))

        conn = get_db_connection()
        user = conn.execute(
            "SELECT * FROM users WHERE email = ? AND password = ?", (email, password)
        ).fetchone()
        conn.close()

        # If user exists and credentials are correct
        if user:
            flash("Login successful!", "success")
            return redirect(url_for("dashboard"))  # redirect to a dashboard page
        else:
            flash("Invalid email or password", "error")
            return redirect(url_for("login"))

    return render_template("login.html")
