from flask import Blueprint

dashboard = Blueprint(
    "dashboard",
    __name__,
    template_folder="templates/dashboard",
    static_folder="static",
    url_prefix="/dashboard",
)


@dashboard.route("/home", methods=["GET", "POST"])
def home():
    return "Hello World!"