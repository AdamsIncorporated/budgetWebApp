import logging
import os
import secrets
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()


class Config:
    # General Config
    FLASK_APP = "run.py"
    SECRET_KEY = secrets.token_hex(16)
    REACT_APP_URL = os.getenv("REACT_APP_URL", "http://localhost:3000")

    # Flask Logging
    LOGGING_LEVEL = logging.DEBUG
    LOGGING_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    LOGGING_LOCATION = os.path.join(os.path.dirname(__file__), "../app.log")

    # Flask Mail Server
    MAIL_SERVER = os.environ.get("MAIL_SERVER")
    MAIL_PORT = os.environ.get("MAIL_PORT")
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.environ.get("EMAIL_USER")
    MAIL_PASSWORD = os.environ.get("EMAIL_PASS")

    # Flask-Session
    SESSION_TYPE = "redis"
    SESSION_PERMANENT = True
    SESSION_USE_SIGNER = True
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    SESSION_COOKIE_SAMESITE = "Strict"

    # CSRF TOKEN SESSION
    WTF_CSRF_SECRET_KEY = secrets.token_hex(16)
    WTF_CSRF_ENABLED = True

    @staticmethod
    def init_app_logging(app):
        logging.basicConfig(
            level=Config.LOGGING_LEVEL,
            format=Config.LOGGING_FORMAT,
            handlers=[
                logging.FileHandler(Config.LOGGING_LOCATION),
                logging.StreamHandler(),
            ],
        )
