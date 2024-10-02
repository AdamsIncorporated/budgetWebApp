from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    flash,
    url_for,
    current_app,
)
from repositories.db_manager import DatabaseManager
from .forms import LoginForm
import hashlib


auth = Blueprint(
    "auth",
    __name__,
    template_folder="templates/auth",
    static_folder="static",
    url_prefix="/auth",
)


@auth.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    
    if request.method == "POST":

        if form.validate_on_submit():
            email = request.form["email"]
            password = request.form["password"]
            sha_512_password = hashlib.sha512(password.encode()).hexdigest()

            db = DatabaseManager("data/main.db", logger=current_app.logger)
            user = db.execute(
                query="SELECT * FROM User WHERE email = ? AND password = ?",
                params=(email, sha_512_password),
            )
            db.close_connection()

            # If user exists and credentials are correct
            if user:
                flash("Login successful!", "dashboard")
                return redirect(
                    url_for("success_login")
                )  # redirect to a dashboard page
            else:
                flash("Invalid email or password", "error")
                return redirect(url_for("login"))

    return render_template("login.html", form=form)
