"""Automated tests for the homepage and status endpoints."""

from app import create_app


def test_homepage_loads():
    """The homepage should return HTML and include the project title."""
    client = create_app().test_client()

    response = client.get("/")

    assert response.status_code == 200
    assert b"From a code" in response.data
    assert b"CI/CD Pipeline Project" in response.data


def test_health_endpoint_is_healthy():
    """Render's health check should receive a healthy response."""
    client = create_app().test_client()

    response = client.get("/health")

    assert response.status_code == 200
    assert response.get_json() == {"status": "healthy"}


def test_api_status_includes_application_metadata(monkeypatch):
    """Status includes safe deployment metadata and a short commit ID."""
    monkeypatch.setenv("APP_ENV", "production")
    monkeypatch.setenv("APP_VERSION", "1.2.3")
    monkeypatch.setenv("RENDER_GIT_COMMIT", "abcdef0123456789")
    client = create_app().test_client()

    response = client.get("/api/status")

    assert response.status_code == 200
    assert response.get_json() == {
        "service": "CI/CD Pipeline Demo",
        "status": "operational",
        "environment": "production",
        "version": "1.2.3",
        "commit": "abcdef0",
    }


def test_api_status_uses_safe_local_defaults(monkeypatch):
    """Local development works without Render-specific environment values."""
    monkeypatch.delenv("APP_ENV", raising=False)
    monkeypatch.delenv("APP_VERSION", raising=False)
    monkeypatch.delenv("RENDER_GIT_COMMIT", raising=False)
    client = create_app().test_client()

    response = client.get("/api/status")

    assert response.status_code == 200
    assert response.get_json()["environment"] == "development"
    assert response.get_json()["version"] == "1.0.0"
    assert response.get_json()["commit"] is None
