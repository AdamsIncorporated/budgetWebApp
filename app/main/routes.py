from flask import Blueprint, render_template
from app import db
from sqlalchemy import text

main = Blueprint(
    "main",
    __name__,
    template_folder="templates/main",
    static_folder="static",
    url_prefix="/",
)


def get_all_business_units():
    query = text(
        "SELECT DISTINCT BusinessUnitId, BusinessUnit FROM BusinessUnit ORDER BY BusinessUnitId;"
    )
    result = db.session.execute(query).fetchall()
    return result

def get_all_fiscal_years():
    query = text(
        "SELECT DISTINCT FiscalYear FROM JournalEntry ORDER BY FiscalYear;"
    )
    result = db.session.execute(query).fetchall()
    return result


picklist = {
    "BUSINESS_UNIT_IDS": get_all_business_units(),
    "FISCAL_YEARS": get_all_fiscal_years(),
}


@main.route("/")
@main.route("/home")
def home():
    return render_template("index.html", picklist=picklist)
