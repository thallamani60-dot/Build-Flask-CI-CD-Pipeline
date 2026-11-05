"""WSGI entry point used by Gunicorn and local Flask commands."""

from app import create_app

app = create_app()
