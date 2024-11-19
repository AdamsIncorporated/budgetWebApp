from flask import Flask, jsonify, request, session
from app.config import Config
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_wtf.csrf import CSRFProtect, generate_csrf

# Initialize extensions globally
bcrypt = Bcrypt()
login_manager = LoginManager()
mail = Mail()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    Config.init_app_logging(app)
    csrf = CSRFProtect(app)

    @app.before_request
    def before_request():
        state_changing_methods = [
            "POST",
            "PUT",
            "PATCH",
            "DELETE",
        ]

        if request.method in state_changing_methods:
            csrf.protect()

    @app.route("/get-csrf-token", methods=["GET"])
    def get_csrf_token():
        csrf_token = generate_csrf()
        session["_csrf_token"] = csrf_token
        return jsonify({"csrf_token": csrf_token})

    # Associate extensions with the app
    bcrypt.init_app(app)
    login_manager.init_app(app)
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
