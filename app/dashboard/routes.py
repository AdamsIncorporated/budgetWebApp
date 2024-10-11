from flask import Blueprint, render_template
from flask_login import login_required, current_user
import base64

dashboard = Blueprint(
    "dashboard",
    __name__,
    template_folder="templates/dashboard",
    static_folder="static",
    url_prefix="/dashboard",
)


@dashboard.route("/home", methods=["GET", "POST"])
@login_required
def home():
    image_file = None
    if current_user.image_file:
        image_file = base64.b64encode(current_user.image_file).decode('utf-8')
        
    return render_template("dashboard.html", image_file=image_file)

@dashboard.route("/add-users", methods=["GET", "POST"])
@login_required
def add_users():
    return render_template("add_users.html")