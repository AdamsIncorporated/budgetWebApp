from flask import Flask, request
from app.config import Config
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_wtf.csrf import CSRFProtect, generate_csrf
from flask_cors import CORS
from datetime import datetime, timedelta
import json

# Initialize extensions globally
bcrypt = Bcrypt()
login_manager = LoginManager()
mail = Mail()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    Config.init_app_logging(app)
    csrf = CSRFProtect(app)
    csrf.init_app(app)
    CORS(app, origins=["http://localhost:3000"], supports_credentials=True)

    @app.after_request
    def after_request(response):
        if "csrf_token" not in request.cookies:
            csrf_token = generate_csrf()
            response.headers["X-CSRFToken"] = csrf_token
            request.csrf_included = True

        return response

    # Associate extensions with the app
    bcrypt.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    mail.init_app(app)

    with app.app_context():
        from app.main.routes import main
        from app.auth.routes import auth
        from app.budget.routes import budget
        from app.dashboard.routes import dashboard

        app.register_blueprint(auth)
        app.register_blueprint(main)
        app.register_blueprint(budget)
        app.register_blueprint(dashboard)

    return app
