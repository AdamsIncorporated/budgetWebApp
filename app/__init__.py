from flask import Flask
from app.config import Config
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy

# Initialize extensions globally
bcrypt = Bcrypt()
login_manager = LoginManager()
mail = Mail()
db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    Config.init_app(app)

    # Associate extensions with the app
    bcrypt.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "login"
    login_manager.login_message_category = "info"
    mail.init_app(app)

    with app.app_context():
        from app.main.routes import main
        from app.auth.routes import auth
        from app.budget.routes import budget
        from app.dashboard.routes import dashboard
        from app.errors.handlers import errors

        app.register_blueprint(auth)
        app.register_blueprint(main)
        app.register_blueprint(budget)
        app.register_blueprint(dashboard)
        app.register_blueprint(errors)

    return app
