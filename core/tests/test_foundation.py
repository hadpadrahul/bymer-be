from django.conf import settings
from rest_framework.test import APIClient


def test_health_endpoint_returns_ok():
    client = APIClient()

    response = client.get("/api/health/")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_schema_endpoint_is_available():
    client = APIClient()

    response = client.get("/api/schema/")

    assert response.status_code == 200


def test_static_and_media_settings_are_configured():
    assert settings.STATIC_URL
    assert settings.STATIC_ROOT
    assert settings.MEDIA_URL
    assert settings.MEDIA_ROOT
