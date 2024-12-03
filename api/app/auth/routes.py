from flask import (
    url_for,
    flash,
    request,
    Blueprint,
    jsonify,
    current_app,
)
from app import bcrypt, mail
from repositories.models import User, UserRegistration
from repositories.db import Database
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message
from dataclasses import asdict
from datetime import timedelta


auth = Blueprint(
    name="auth",
    import_name=__name__,
    url_prefix="/auth",
)


@auth.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return (
            jsonify({"message": "Cookie generated for CSRF Token"}),
            200,
        )

    if request.method == "POST":
        data = request.get_json()
        user = UserRegistration(**data)

        try:
            user.validate()
        except ValueError as e:
            return jsonify({"message": str(e)}), 409

        hashed_password = bcrypt.generate_password_hash(data["password"])
        data["password"] = hashed_password
        data.pop("confirm_password")
        insert_data = asdict(User(**data))
        insert_data.pop("id")
        Database().create(table="user", data=insert_data)
        return jsonify({"message": "User created."}), 200


@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return (
            jsonify({"message": "Cookie generated for CSRF Token"}),
            200,
        )

    elif request.method == "POST":
        data = request.get_json()

        if current_user.is_authenticated:
            user_data = current_user.to_dict()
            user_data.pop("Password", None)
            return (
                jsonify({"message": "User already authenticated", "user": user_data}),
                200,
            )

        else:
            result = Database().read(
                "SELECT * FROM User WHERE Email = :email LIMIT 1",
                {"email": data["email"]},
            )
            user = asdict(User(**result))

            if not user:
                return jsonify({"message": "user not found"}), 404

            if bcrypt.check_password_hash(user["Password"], data["password"]):
                duration = timedelta(weeks=current_app["PERMANENT_SESSION_LIFETIME"])
                login_user(user, duration=duration)
                user_data = current_user.to_dict()
                user_data.pop("Password", None)
                return jsonify({"message": "Login successful", "user": user_data}), 200

            return jsonify({"message": "Invalid credentials"}), 401


@auth.route("/logout")
def logout():
    logout_user()
    return jsonify({"message": "User logged out."}), 200


@auth.route("/account", methods=["GET", "POST"])
@login_required
def account():
    if request.method == "GET":
        id = request.data.get("Id")

        if not id:
            return jsonify({"message": "Id not provided"}), 500

        query = "SELECT UserName, Email, FirstName, LastName, ImageFile FROM User WHERE Id = :Id"
        result = Database().read(sql=query, params={"Id": id})
        user = asdict(User(**result))
        return jsonify({"message": "User data response", "user": user}), 200

    if request.method == "POST":
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


def send_reset_email(user: User):
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


@auth.route("/reset-password", methods=["GET", "POST"])
def reset_request():
    if request.method == "GET":
        return (
            jsonify({"message": "Cookie generated for CSRF Token"}),
            200,
        )

    if request.method == "POST":
        data = request.get_json()
        result = Database().read(
            sql='SELECT * FROM "user" WHERE email = %s LIMIT 1',
            params=(data["email"],),
        )

        if not result:
            return jsonify({"message": "User not found"}), 404

        user = User(**result)
        send_reset_email(user)

        return (
            jsonify({"message": "Email sent for authentification"}),
            200,
        )


@auth.route("/reset-password-token/<token>", methods=["GET", "POST"])
def reset_token(token):
    user = User.verify_reset_token(token)

    if user is None:
        return (
            jsonify({"message": "That is an invalid or expired token"}),
            200,
        )

    if request.method == "GET":
        return (
            jsonify({"message": "Cookie generated for CSRF Token"}),
            200,
        )

    if request.method == "POST":
        data = request.get_json()
        hashed_password = bcrypt.generate_password_hash(data["password"])
        Database().update(
            table="user",
            data={"password": hashed_password},
            where="id = %s",
            where_params=(user.id,),
        )
        return (
            jsonify({"message": "Cookie generated for CSRF Token"}),
            200,
        )
