from flask import Flask
from .config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)  # Load configuration from Config class
    
    # Initialize logging
    Config.init_app(app)
    
    with app.app_context():
        # Import routes
        from .routes import main
        app.register_blueprint(main)
        
    return app