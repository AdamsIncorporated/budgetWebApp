from flask import Blueprint, render_template

dashboard = Blueprint(
    "dashboard",
    __name__,
    template_folder="templates/dashboard",
    static_folder="static",
    url_prefix="/dashboard",
)


@dashboard.route("/home", methods=["GET", "POST"])
def home():
    return render_template("dashboard.html")