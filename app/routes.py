from flask import Blueprint, render_template

main = Blueprint("main", __name__)


@main.route("/")
@main.route("/budget-entry")
def home():
    return render_template("index.html")
