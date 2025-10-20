import os
import logging
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf import CSRFProtect
from flask_cors import CORS
from flask_compress import Compress
from config import Config

# --- Initialize core extensions ---
db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()
compress = Compress()

def create_app(config_class=Config):
    """Flask app factory pattern."""
    app = Flask(__name__, static_folder='static', template_folder='templates')
    app.config.from_object(config_class)

    # --- Instance & database folder setup ---
    instance_path = os.path.join(app.root_path, '..', 'instance')
    os.makedirs(instance_path, exist_ok=True)
    db_path = os.path.join(instance_path, 'database.db')
    if not os.path.exists(db_path):
        open(db_path, 'a').close()  # ensure file exists

    # --- Initialize extensions ---
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    csrf.init_app(app)
    CORS(app)
    compress.init_app(app)

    # --- Register Blueprints ---
    from .auth import auth_bp
    from .main import main_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)

    # --- Create database tables on first run ---
    with app.app_context():
        try:
            from . import models
            db.create_all()
            app.logger.info('Database tables created successfully.')
        except Exception as e:
            app.logger.error(f'Error creating database tables: {e}')

    # --- CLI & context setup ---
    @app.shell_context_processor
    def make_shell_context():
        from .models import User, Turf, Slot, Booking
        return {'db': db, 'User': User, 'Turf': Turf, 'Slot': Slot, 'Booking': Booking}

    # --- Simple Error Handlers (temporary fix) ---
    @app.errorhandler(404)
    def not_found_error(error):
        return """
        <!DOCTYPE html>
        <html>
        <head>
            <title>404 - Page Not Found</title>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
        </head>
        <body class="bg-light">
            <div class="container text-center my-5 py-5">
                <h1 class="display-1">404</h1>
                <h2>Page Not Found</h2>
                <p class="lead">The page you're looking for doesn't exist.</p>
                <a href="/" class="btn btn-primary">Go Home</a>
            </div>
        </body>
        </html>
        """, 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return """
        <!DOCTYPE html>
        <html>
        <head>
            <title>500 - Internal Server Error</title>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
        </head>
        <body class="bg-light">
            <div class="container text-center my-5 py-5">
                <h1 class="display-1">500</h1>
                <h2>Internal Server Error</h2>
                <p class="lead">Something went wrong on our end.</p>
                <a href="/" class="btn btn-primary">Go Home</a>
            </div>
        </body>
        </html>
        """, 500

    # --- Logging setup ---
    log_file = os.path.join(instance_path, 'app.log')
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.INFO)
    formatter = logging.Formatter(
        '%(asctime)s [%(levelname)s] %(module)s: %(message)s'
    )
    file_handler.setFormatter(formatter)
    app.logger.addHandler(file_handler)
    app.logger.info('App startup complete.')

    return app