from flask import Blueprint, render_template

main = Blueprint("main", __name__, template_folder="templates/main", static_folder="static")


@main.route("/")
@main.route("/home")
def home():
    return render_template("index.html",)


