from flask import Blueprint, render_template
from app import db
from sqlalchemy import text
import base64
from flask_login import current_user

main = Blueprint(
    "main",
    __name__,
    template_folder="templates/main",
    static_folder="static",
    url_prefix="/",
)


def get_all_business_units(user_id=None):
    if user_id:  # not admin so we query very specific business units
        query = text(
            f"SELECT DISTINCT b.BusinessUnitId, b.BusinessUnit FROM BusinessUnit b JOIN User_BusinessUnit ub ON ub.BusinessUnitId = b.BusinessUnitId WHERE ub.UserId = {user_id} ORDER BY b.BusinessUnitId;"
        )
    else:
        query = text(
            "SELECT DISTINCT BusinessUnitId, BusinessUnit FROM BusinessUnit ORDER BY BusinessUnitId;"
        )
    result = db.session.execute(query).fetchall()
    return result


def get_all_fiscal_years():
    query = text("SELECT DISTINCT FiscalYear FROM JournalEntry ORDER BY FiscalYear;")
    result = db.session.execute(query).fetchall()
    return result


@main.route("/")
@main.route("/home")
def home():
    picklist = None
    image_file = None

    if current_user.is_authenticated and current_user.image_file:
        image_file = base64.b64encode(current_user.image_file).decode("utf-8")

        if current_user.is_root_user:
            picklist = {
                "BUSINESS_UNIT_IDS": get_all_business_units(),
                "FISCAL_YEARS": get_all_fiscal_years(),
            }
        else:
            picklist = {
                "BUSINESS_UNIT_IDS": get_all_business_units(user_id=current_user.id),
                "FISCAL_YEARS": get_all_fiscal_years(),
            }

    return render_template("index.html", picklist=picklist, image_file=image_file)
