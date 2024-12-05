from repositories.models import User, UserRegistration
from flask import current_app
from flask_bcrypt import bcrypt
from flask_login import current_user
from dataclasses import asdict
from flask_mail import Message
import time
from app import mail
import jwt


def convert_user_registration_data_to_insert_data(
    user_registration: UserRegistration,
) -> dict:
    # generate a hashed password
    hashed_password = bcrypt.generate_password_hash(user_registration.password).decode(
        "utf-8"
    )
    user_registration.password = hashed_password

    # apply user creator id if already logged in while creating another user
    if current_user.is_authenticated:
        user_creator_id = current_user.id
        user_registration.user_creator_id = user_creator_id

    # remove confirm password for binding to user class
    user_registration_dict = asdict(user_registration)
    user_registration_dict.pop("confirm_password")

    # bind the scrubbed data to the user class
    insert_data = asdict(User(**user_registration_dict))
    insert_data.pop("id")

    return insert_data


def send_admin_registration_email(proposed_user: User):
    payload = {
        "user": proposed_user.__dict__,
        "exp": time.time() + 18000,
    }
    token = jwt.encode(payload, current_app.config["SECRET_KEY"], algorithm="HS256")
    sender = current_app.config["MAIL_USERNAME"]
    recipents = [current_app.config["ROOT_EMAIL_USER"]]  # must be a list
    msg = Message(
        "Budget Web App",
        sender=sender,
        recipients=recipents,
    )
    react_url = f"{current_app.config['REACT_APP_URL']}/auth/register-admin/{token}"
    msg.body = f"""

    🚨THIS EMAIL WAS SENT BY THE USER ACCOUNT SAMUEL.GRANT.ADAMS@GMAIL.COM SMTP SERVER
    PLEASE IGNORE AS THIS IS FOR TESTING ADMIN CREATION🚨

    To fully register the admin user, visit the following link:
    
    {react_url}

    If you did not make this request then simply ignore this email and no changes will be made.
    """
    mail.send(msg)


def send_reset_email(user: User):
    token = user.get_reset_token()
    sender = current_app.config["MAIL_USERNAME"]
    recipents = [user.email]  # must be a list
    msg = Message(
        "Password Reset Request",
        sender=sender,
        recipients=recipents,
    )
    react_url = (
        f"{current_app.config['REACT_APP_URL']}/auth/reset-password-token/{token}"
    )
    msg.body = f"""
    To reset your password, visit the following link:
    
    {react_url}

    If you did not make this request then simply ignore this email and no changes will be made.
    """
    mail.send(msg)
