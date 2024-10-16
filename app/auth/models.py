from app import db, login_manager
from flask import current_app
from flask_login import UserMixin
import jwt
from datetime import datetime, timedelta


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
    first_name = db.Column("FirstName", db.String(20), nullable=False)
    last_name = db.Column("LastName", db.String(20), nullable=False)
    date_created = db.Column(
        "DateCreated",
        db.DateTime,
        nullable=False,
        default=db.func.current_timestamp(),
    )
    is_root_user = db.Column("IsRootUser", db.Integer, nullable=False, default=0)

    def get_reset_token(self, expires_sec=1800):
        # Create a payload with the user ID and expiration time
        payload = {
            "user_id": self.id,
            "exp": datetime.utcnow() + timedelta(seconds=expires_sec),
        }
        # Encode the payload using the secret key
        return jwt.encode(payload, current_app.config["SECRET_KEY"], algorithm="HS256")

    @staticmethod
    def verify_reset_token(token):
        try:
            # Decode the token using the secret key
            payload = jwt.decode(
                token, current_app.config["SECRET_KEY"], algorithms=["HS256"]
            )
            user_id = payload["user_id"]
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
            return None
        return User.query.get(user_id)