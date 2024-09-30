# app/__init__.py
from flask import Flask
from .config import Config
import secrets
import random


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)  # Load configuration from Config class

    Config.init_app(app)
    app.config["SECRET_KEY"] = secrets.token_hex(16)

    # Define global variables using a context processor
    @app.context_processor
    def inject_global_variables():
        return {"random_three_digit": lambda: random.randint(100, 999)}

    with app.app_context():
        from app.main.routes import main

        app.register_blueprint(main)

    return app
