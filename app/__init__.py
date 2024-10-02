from flask import Flask
from .config import Config
import secrets


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    Config.init_app(app)
    app.config["SECRET_KEY"] = secrets.token_hex(16)

    with app.app_context():
        from app.main.routes import main
        from app.auth.routes import auth

        app.register_blueprint(auth)
        app.register_blueprint(main)

    return app
