from app.app import app


def test_home():
    client = app.test_client()

    response = client.get("/")

    assert response.status_code == 200
    assert response.data == b"Secure CI/CD Pipeline Lab"


def test_health_without_database():
    client = app.test_client()

    response = client.get("/health")

    assert response.status_code in (200, 503)