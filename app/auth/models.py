from itsdangerous import (
    URLSafeTimedSerializer as Serializer,
    BadSignature,
    SignatureExpired,
)
from app import db, login_manager
from flask import current_app
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    __tablename__ = "User"

    id = db.Column("Id", db.Integer, primary_key=True)
    username = db.Column("Username", db.String(20), unique=True, nullable=False)
    email = db.Column("Email", db.String(120), unique=True, nullable=False)
    password = db.Column("Password", db.String(60), nullable=False)
    image_file = db.Column("ImageFile", db.LargeBinary, nullable=True)
    first_name = db.Column("FirstName", db.String(20), nullable=True)
    last_name = db.Column("LastName", db.String(20), nullable=True)
    date_created = db.Column(
        "DateCreated",
        db.DateTime,
        nullable=False,
        default=db.func.current_timestamp(),
    )
    is_root_user = db.Column(
        "IsRootUser", db.LargeBinary, nullable=False, default=False
    )

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config["SECRET_KEY"], expires_sec)
        return s.dumps({"user_id": self.id}).decode("utf-8")

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config["SECRET_KEY"])
        try:
            user_id = s.loads(token)["user_id"]
        except (BadSignature, SignatureExpired):
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"
