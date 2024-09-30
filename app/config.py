import logging
import os

class Config:
    """Base configuration class."""
    LOGGING_LEVEL = logging.DEBUG
    LOGGING_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    LOGGING_LOCATION = os.path.join(os.path.dirname(__file__), '../app.log')  # Log file location

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
