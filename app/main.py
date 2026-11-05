"""Page and status endpoints for the CI/CD demonstration app."""

import os

from flask import Blueprint, jsonify, render_template

main = Blueprint("main", __name__)


@main.get("/")
def index():
    """Render the project homepage."""
    return render_template("index.html")


@main.get("/health")
def health():
    """Return a small readiness response for Render and monitoring tools."""
    return jsonify(status="healthy"), 200


@main.get("/api/status")
def api_status():
    """Return non-sensitive application and deployment metadata."""
    commit = os.getenv("RENDER_GIT_COMMIT", "")
    return jsonify(
        service="CI/CD Pipeline Demo",
        status="operational",
        environment=os.getenv("APP_ENV", "development"),
        version=os.getenv("APP_VERSION", "1.0.0"),
        commit=commit[:7] if commit else None,
    ), 200
