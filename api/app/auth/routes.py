import base64
from flask import render_template, url_for, flash, redirect, request, Blueprint, jsonify
from app import bcrypt, mail
from repositories.models import User
from repositories.db import Database
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message
from dataclasses import asdict


auth = Blueprint(
    name="auth",
    import_name=__name__,
    url_prefix="/auth",
)


@auth.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        pass

    form = request.form()
    hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
    user = User(
        username=form.username.data,
        email=form.email.data,
        first_name=form.first_name.data,
        last_name=form.last_name.data,
        password=hashed_password,
        is_root_user=1 if form.is_root_user.data else 0,
    )
    # db.session.add(user)
    # db.session.commit()
    return jsonify({"message": "User created."}), 200


@auth.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    result = Database().read(
        "SELECT * FROM User WHERE Email = :email LIMIT 1", {"email": data["email"]}
    )
    user = asdict(User(**result))
    if user and bcrypt.check_password_hash(user["Password"], data["password"]):
        return jsonify({"message": "Login successful", "user": user}), 200
    return jsonify({"message": "Invalid credentials"}), 401


@auth.route("/logout")
def logout():
    logout_user()
    return jsonify({"message": "User logged out."}), 200


@auth.route("/account", methods=["POST"])
@login_required
def account():
    form = request.form

    if form.picture.data:
        picture = form.picture.data
        binary_data = picture.read()

        if len(binary_data) > 1 * 1024 * 1024:
            flash("", "error")
            return jsonify({"message": "File size exceeds the 1MB limit."}), 413

        image_file = binary_data

    username = form.username.data
    email = form.email.data
    first_name = form.first_name.data
    last_name = form.last_name.data


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message(
        "Password Reset Request",
        sender="samuel.grant.adams@gmail.com",
        recipients=[user.email],
    )
    msg.body = f"""To reset your password, visit the following link:
    {url_for('auth.reset_token', token=token, _external=True)}

    If you did not make this request then simply ignore this email and no changes will be made.
    """
    mail.send(msg)


@auth.route("/reset_password", methods=["GET", "POST"])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.home"))

    form = request.form()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash(
            "An email has been sent with instructions to reset your password.",
            "success",
        )

        return redirect(url_for("auth.login"))

    return render_template("reset_request.html", title="Reset Password", form=form)


@auth.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.home"))

    user = User.verify_reset_token(token)

    if user is None:
        flash("That is an invalid or expired token", "error")

        return redirect(url_for("auth.reset_request"))

    form = request.form()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode(
            "utf-8"
        )
        user.password = hashed_password
        return redirect(url_for("auth.login"))

    return render_template("reset_token.html", title="Reset Password", form=form)
