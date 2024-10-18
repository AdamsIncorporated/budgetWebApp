from flask import Blueprint, render_template, redirect, flash, url_for, request
from flask_login import login_required, current_user
import base64
from app import db
from repositories.models import MasterEmail, BusinessUnit, UserBusinessUnit, User
from .forms import MasterEmailForm, UserBusinessUnits
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


@dashboard.route("/home")
@login_required
def home():
    image_file = None
    if current_user.image_file:
        image_file = base64.b64encode(current_user.image_file).decode("utf-8")

    return render_template("dashboardHome.html", image_file=image_file)


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


@dashboard.route("/add-users")
@login_required
def add_users():
    master_emails = MasterEmail.query.all()
    image_file = None
    if current_user.image_file:
        image_file = base64.b64encode(current_user.image_file).decode("utf-8")

    return render_template(
        "addUsers.html", master_emails=master_emails, image_file=image_file
    )


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
            
            # query users to get id
            user_id = User.query.filter_by(email=form.email.data).first_or_404().id

            for row in form.user_business_units.data:
                if row.get("is_business_unit_selected"):
                    business_unit_id = int(row.get("business_unit_id"))
                    new_user_business_unit = UserBusinessUnit(
                        user_id=user_id, business_unit_id=business_unit_id
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

    return render_template("modal/createModal.html", form=form)


@dashboard.route("/edit", methods=["GET", "POST"])
@login_required
def edit():
    form = UserBusinessUnits()

    if request.method == "GET":
        user_id = int(request.args.get("id"))
        master_email = MasterEmail.query.filter_by(id=user_id).first()

        query = queries["user_business_units"](user_id=user_id)
        user_business_units = db.session.execute(text(query)).fetchall()

        data = {
            "user_id": user_id,
            "email": master_email.email,
            "date_created": master_email.date_created,
            "user_business_units": [
                {
                    "id": id,
                    "business_unit_id": business_unit_id,
                    "business_unit": business_unit,
                    "is_business_unit_selected": is_business_unit_selected,
                }
                for id, business_unit_id, business_unit, is_business_unit_selected in user_business_units
            ],
        }
        form.process(data=data)

    if request.method == "POST":
        if form.validate_on_submit():
            user_id = int(form.user_id.data)
            current_units = UserBusinessUnit.query.filter_by(user_id=user_id).all()
            current_unit_ids = {(ub.id, ub.business_unit_id) for ub in current_units}

            selected_units = {
                (row["id"], row["business_unit_id"])
                for row in form.user_business_units.data
                if row["is_business_unit_selected"]
            }
            units_to_delete = current_unit_ids - selected_units
            units_to_add = selected_units - current_unit_ids

            # Delete unselected business units
            if units_to_delete:
                for unit_id, business_unit_id in units_to_delete:
                    UserBusinessUnit.query.filter_by(
                        id=unit_id, user_id=user_id
                    ).delete(synchronize_session=False)

            # Add new selected business units
            for unit_id, business_unit_id in units_to_add:
                new_unit = UserBusinessUnit(
                    user_id=user_id, business_unit_id=business_unit_id
                )
                db.session.add(new_unit)

            db.session.commit()

            flash(f"Successfully updated {form.email.data} user!", "success")

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

    return render_template("modal/editModal.html", form=form)


@dashboard.route("/delete", methods=["GET", "POST"])
@login_required
def delete():
    id = int(request.args.get("id"))
    data = MasterEmail.query.filter_by(id=id).first()

    if request.method == "POST":
        master_email = MasterEmail.query.get(id)

        if data:
            db.session.delete(master_email)
            db.session.commit()
            flash("Successfully deleted user!", "success")

            return redirect(url_for("dashboard.add_users"))

        else:
            flash("User not found!", "error")

            return redirect(url_for("dashboard.add_users"))

    return render_template("modal/deleteModal.html", data=data)
