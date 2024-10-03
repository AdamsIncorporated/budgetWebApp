import logging
import os
import secrets
from dotenv import load_dotenv
import ssl

load_dotenv()


class Config:
    """Base configuration class."""

    LOGGING_LEVEL = logging.DEBUG
    LOGGING_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    LOGGING_LOCATION = os.path.join(os.path.dirname(__file__), "../app.log")
    SECRET_KEY = secrets.token_hex(16)
    MAIL_SERVER = os.environ.get("MAIL_SERVER")
    MAIL_PORT = os.environ.get("MAIL_PORT")
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.environ.get("EMAIL_USER")
    MAIL_PASSWORD = os.environ.get("EMAIL_PASS")
    SQLALCHEMY_DATABASE_URI = "sqlite:///C:/Projects/budgetWebApp/data/main.db"
    # context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    # context.load_cert_chain(
    #     certfile="path/to/your/certificate.crt", keyfile="path/to/your/private.key"
    # )
    # app.run(ssl_context=context, host="0.0.0.0", port=443)

    @staticmethod
    def init_app(app):
        """Initialize logging."""
        logging.basicConfig(
            level=Config.LOGGING_LEVEL,
            format=Config.LOGGING_FORMAT,
            handlers=[
                logging.FileHandler(Config.LOGGING_LOCATION),  # Log to file
                logging.StreamHandler(),  # Log to console
            ],
        )
