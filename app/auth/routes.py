import base64
from flask import render_template, url_for, flash, redirect, request, Blueprint
from app import bcrypt, mail
from app.auth.forms import (
    RegistrationForm,
    LoginForm,
    UpdateAccountForm,
    RequestResetForm,
    ResetPasswordForm,
)
from repositories.models import User
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message
from app import db

auth = Blueprint(
    "auth",
    __name__,
    template_folder="templates/auth",
    static_folder="static",
    url_prefix="/auth",
)


@auth.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.home"))

    form = RegistrationForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode(
            "utf-8"
        )
        user = User(
            username=form.username.data,
            email=form.email.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            password=hashed_password,
            is_root_user=1,
        )
        db.session.add(user)
        db.session.commit()
        flash("Your account has been created! You are now able to log in", "success")
        return redirect(url_for("auth.login"))
    return render_template("register.html", title="Register", form=form)


@auth.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.home"))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get("next")
            return redirect(next_page) if next_page else redirect(url_for("dashboard.home"))
        else:
            flash("Login Unsuccessful. Please check email and password", "error")
    return render_template("login.html", title="Login", form=form)


@auth.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("main.home"))


@auth.route("/account", methods=["GET", "POST"])
@login_required
def account():
    form = UpdateAccountForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            if form.picture.data:
                picture = form.picture.data
                binary_data = picture.read()
                
                if len(binary_data) > 1 * 1024 * 1024:
                    flash("File size exceeds the 1MB limit", "error")
                    return redirect(url_for("auth.account"))
                
                current_user.image_file = binary_data
                
            current_user.username = form.username.data
            current_user.email = form.email.data
            current_user.first_name = form.first_name.data
            current_user.last_name = form.last_name.data
            db.session.commit()
            flash("Your account has been updated!", "success")

            return redirect(url_for("auth.account"))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name

    image_file = None
    if current_user.image_file:
        image_file = base64.b64encode(current_user.image_file).decode('utf-8')

    return render_template(
        "account.html", title="Account", image_file=image_file, form=form
    )


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message(
        "Password Reset Request", sender="samuel.grant.adams@gmail.com", recipients=[user.email]
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

    form = RequestResetForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash(
            "An email has been sent with instructions to reset your password.", "success"
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

    form = ResetPasswordForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode(
            "utf-8"
        )
        user.password = hashed_password
        db.session.commit()
        flash("Your password has been updated! You are now able to log in", "success")

        return redirect(url_for("auth.login"))

    return render_template("reset_token.html", title="Reset Password", form=form)