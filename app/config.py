import logging
import os
import secrets
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base configuration class."""
    LOGGING_LEVEL = logging.DEBUG
    LOGGING_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    LOGGING_LOCATION = os.path.join(os.path.dirname(__file__), '../app.log')
    SECRET_KEY = secrets.token_hex(16)
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///C:/Projects/budgetWebApp/data/main.db'

    @staticmethod
    def init_app(app):
        """Initialize logging."""
        logging.basicConfig(
            level=Config.LOGGING_LEVEL,
            format=Config.LOGGING_FORMAT,
            handlers=[
                logging.FileHandler(Config.LOGGING_LOCATION),  # Log to file
                logging.StreamHandler()  # Log to console
            ]
        )
        
        
