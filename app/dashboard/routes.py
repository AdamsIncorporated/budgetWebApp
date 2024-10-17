from flask import Blueprint, render_template, redirect, flash, url_for, request
from flask_login import login_required, current_user
import base64
from app import db
from repositories.models import MasterEmail, BusinessUnit, UserBusinessUnit
from .forms import MasterEmailForm, UserBusinessUnits
from sqlalchemy.orm import joinedload, aliased
from flask import jsonify
from sqlalchemy import text
from repositories.queries import queries


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
        image_file = base64.b64encode(current_user.image_file).decode("utf-8")

    return render_template("dashboard.html", image_file=image_file)


@dashboard.route("/account-actuals-timeline")
def account_actuals_timeline():
    result = (
        db.session.execute(text(queries["account_actuals_timeline"])).mappings().all()
    )
    result_dicts = [dict(row) for row in result]
    return jsonify(records=result_dicts)


@dashboard.route("/budget-pie-chart")
def budget_pie_chart():
    result = db.session.execute(text(queries["budget_pie_chart"])).mappings().all()
    result_dicts = [dict(row) for row in result]
    return jsonify(records=result_dicts)


@dashboard.route("/add-users", methods=["GET", "POST"])
@login_required
def add_users():
    master_emails = MasterEmail.query.all()

    return render_template("add_users.html", master_emails=master_emails)


@dashboard.route("/create", methods=["GET", "POST"])
@login_required
def create():
    form = MasterEmailForm()

    if request.method == "GET":
        query = (
            db.session.query(BusinessUnit.business_unit_id, BusinessUnit.business_unit)
            .distinct()
            .order_by(BusinessUnit.business_unit_id)
        )
        results = query.all()
        data = {"user_business_units": results}
        form.process(data=data)

    if request.method == "POST":
        if form.validate_on_submit():
            new_email = MasterEmail(
                email=form.email.data,
                user_creator_id=current_user.id,
            )
            db.session.add(new_email)
            db.session.commit()
            new_email_id = new_email.id

            for row in form.user_business_units.data:
                if row.get("is_business_unit_selected"):
                    business_unit_id = int(row.get("business_unit_id"))
                    new_user_business_unit = UserBusinessUnit(
                        user_id=new_email_id, business_unit_id=business_unit_id
                    )
                    db.session.add(new_user_business_unit)
            db.session.commit()

            flash(f"User rights for {form.email.data} created successfully!", "success")
            return redirect(url_for("dashboard.add_users"))
        else:
            errors = ". ".join(
                [
                    error
                    for field_errors in form.errors.values()
                    for error in field_errors
                ]
            )
            flash(errors, "error")
            return redirect(url_for("dashboard.add_users"))

    return render_template("createModal.html", form=form)


@dashboard.route("/edit", methods=["GET", "POST"])
def edit():
    form = UserBusinessUnits()

    if request.method == "GET":
        id = int(request.args.get("id"))
        master_email = MasterEmail.query.filter_by(id=id).first()

        query = queries["user_business_units"](user_id=id)
        user_business_units = db.session.execute(text(query)).fetchall()

        data = {
            "email": master_email.email,
            "date_created": master_email.date_created,
            "user_business_units": [
                {
                    "id": ub_id,
                    "business_unit_id": bu_id,
                    "business_unit": bu_name,
                }
                for business_unit_id, business_unit, bu_name in user_business_units
            ],
        }
        form.process(data=data)

    if request.method == "POST":
        if form.validate_on_submit():
            id = form.id.data
            data = MasterEmail.query.get(id)
            data.email = form.email.data
            data.user_creator_id = current_user.id

            # delete all current user business rows by user_id
            db.session.query(UserBusinessUnit).filter_by(user_id=id).delete()
            for row in form.user_business_units.data:
                if row.get("is_business_unit_selected"):
                    new_user_business_unit = UserBusinessUnit(
                        user_id=id,
                        business_unit_id=row.get("business_unit_id"),
                    )
                    db.session.add(new_user_business_unit)

            db.session.commit()
            flash(f"Successfully updated {form.email} user!", "success")

            return redirect(url_for("dashboard.add_users"))
        else:
            errors = ". ".join(
                [
                    error
                    for field_errors in form.errors.values()
                    for error in field_errors
                ]
            )
            flash(errors, "error")
            return redirect(url_for("dashboard.add_users"))

    return render_template("editModal.html", form=form)


@dashboard.route("/delete", methods=["GET", "POST"])
@login_required
def delete():
    form = MasterEmailForm()

    if request.method == "GET":
        id = int(request.args.get("id"))
        master_email_alias = aliased(MasterEmail)
        business_unit_alias = aliased(BusinessUnit)

        data = (
            db.session.query(master_email_alias)  # Start from the MasterEmail model
            .join(business_unit_alias)
            .options(joinedload(master_email_alias.master_email_business_unit))
            .options(joinedload(master_email_alias.master_email_user))
            .filter(master_email_alias.id == id)  # Explicitly using the MasterEmail ID
            .order_by(business_unit_alias.business_unit.asc())
            .first()
        )
        form = MasterEmailForm(obj=data)

    if request.method == "POST" and form.validate_on_submit():
        id = form.id.data
        data = MasterEmail.query.get(id)

        if data:
            db.session.delete(data)
            db.session.commit()
            flash("Successfully deleted user!", "success")
        else:
            flash("User not found!", "error")

        return redirect(url_for("dashboard.add_users"))

    return render_template("deleteModal.html", form=form), 200
