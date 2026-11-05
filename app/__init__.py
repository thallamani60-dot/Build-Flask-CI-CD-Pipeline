"""Flask application package."""

from flask import Flask


def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)

    from app.main import main as main_blueprint

    app.register_blueprint(main_blueprint)
    return app
