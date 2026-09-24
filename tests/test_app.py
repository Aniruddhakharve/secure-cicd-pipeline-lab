from app.app import app


def test_home():
    client = app.test_client()

    response = client.get("/")

    assert response.status_code == 200
    assert b"Secure CI/CD Pipeline Lab" in response.data
    assert b"DevSecOps" in response.data


def test_security_headers():
    client = app.test_client()

    response = client.get("/")

    assert response.headers["X-Content-Type-Options"] == "nosniff"
    assert response.headers["X-Frame-Options"] == "DENY"
    assert "Content-Security-Policy" in response.headers


def test_health_without_database():
    client = app.test_client()

    response = client.get("/health")

    assert response.status_code in (200, 503)