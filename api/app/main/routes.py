from flask import Blueprint, render_template, jsonify
from app import db
from sqlalchemy import text
import base64
from flask_login import current_user
from repositories.queries import queries
from services.current_user_image import image_wrapper
from flask_wtf.csrf import generate_csrf

main = Blueprint(
    "main",
    __name__,
    template_folder="templates/main",
    static_folder="static",
    url_prefix="/main",
)


@main.route("/get-csrf-token", methods=["GET"])
def get_csrf_token():
    csrf_token = generate_csrf()
    return jsonify({"csrf_token": csrf_token})


def get_all_business_units(user_id=None):
    if user_id:  # not admin so we query very specific business units
        query = text(
            queries["fetch_all_regular_user_business_unit_ids"](user_id=user_id)
        )
    else:  # admin so query everything
        query = text(queries["fetch_all_business_unit_ids"])
    result = db.session.execute(query).fetchall()
    return result


@main.route("/")
@main.route("/home")
@image_wrapper
def home(image_file=None):
    picklist = None

    if current_user.is_authenticated and current_user.image_file:

        if current_user.is_root_user:
            picklist = {
                "BUSINESS_UNIT_IDS": get_all_business_units(),
            }
        else:
            picklist = {
                "BUSINESS_UNIT_IDS": get_all_business_units(user_id=current_user.id),
            }

    return render_template("index.html", picklist=picklist, image_file=image_file)
