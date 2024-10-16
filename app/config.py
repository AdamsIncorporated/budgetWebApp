import logging
import os
import secrets
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()


class Config:
    LOGGING_LEVEL = logging.DEBUG
    LOGGING_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    LOGGING_LOCATION = os.path.join(os.path.dirname(__file__), "../app.log")
    SECRET_KEY = secrets.token_hex(16)
    MAIL_SERVER = os.environ.get("MAIL_SERVER")
    MAIL_PORT = os.environ.get("MAIL_PORT")
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.environ.get("EMAIL_USER")
    MAIL_PASSWORD = os.environ.get("EMAIL_PASS")
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.environ.get('DB_PATH')
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)

    @staticmethod
    def init_app(app):
        logging.basicConfig(
            level=Config.LOGGING_LEVEL,
            format=Config.LOGGING_FORMAT,
            handlers=[
                logging.FileHandler(Config.LOGGING_LOCATION),
                logging.StreamHandler(),
            ],
        )
