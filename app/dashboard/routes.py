from flask import Blueprint, render_template, redirect, flash, url_for, request
from flask_login import login_required, current_user
import base64
from app import db
from .models import MasterEmail, BusinessUnit
from .forms import MasterEmailForm
from sqlalchemy.orm import joinedload, aliased


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


@dashboard.route("/add-users", methods=["GET", "POST"])
@login_required
def add_users():
    master_emails = (
        MasterEmail.query.join(BusinessUnit)
        .options(joinedload(MasterEmail.master_email_business_unit))
        .options(joinedload(MasterEmail.master_email_user))
        .order_by(BusinessUnit.business_unit.asc())
        .all()
    )

    return render_template("add_users.html", master_emails=master_emails)

@dashboard.route("/create", methods=["GET", "POST"])
@login_required
def create():
    form = MasterEmailForm()

    if form.validate_on_submit():
        new_email = MasterEmail(
            email=form.email.data,
            user_creator_id=current_user.id,
            business_unit_table_id=form.business_unit_table_id.data,
        )
        db.session.add(new_email)
        db.session.commit()
        flash("Master Email User created successfully!", "success")
        return redirect(url_for("dashboard.add_users"))

    return render_template("createModal.html", form=form)


@dashboard.route("/edit", methods=["GET", "POST"])
@login_required
def edit():
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
        
    if request.method == 'POST' and form.validate_on_submit():
        id = form.id.data
        data = MasterEmail.query.get(id)
        data.email = form.email.data
        data.user_creator_id = current_user.id
        data.business_unit_table_id = form.business_unit_table_id.data
        db.session.commit()
        flash('Successfully updated user!', 'success')
        return redirect(url_for('dashboard.add_users'))

    return render_template("editModal.html", form=form), 200

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
        
    if request.method == 'POST' and form.validate_on_submit():
        id = form.id.data
        data = MasterEmail.query.get(id)
        
        if data:
            db.session.delete(data)
            db.session.commit()
            flash('Successfully deleted user!', 'success')
        else:
            flash('User not found!', 'error')
        
        return redirect(url_for('dashboard.add_users'))

    return render_template("deleteModal.html", form=form), 200
