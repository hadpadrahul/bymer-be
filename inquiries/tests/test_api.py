import pytest
from rest_framework.test import APIClient

from inquiries.models import ContactInquiry, JobApplication


@pytest.fixture
def api_client():
    return APIClient()


@pytest.mark.django_db
def test_contact_form_create(api_client):
    payload = {
        "name": "Jane Doe",
        "email": "jane@example.com",
        "message": "Hello",
        "source_page": "contact-us",
    }

    response = api_client.post("/api/forms/contact/", payload, format="json")

    assert response.status_code == 201
    assert response.json()["success"] is True
    assert ContactInquiry.objects.count() == 1


@pytest.mark.django_db
def test_contact_form_validation_error(api_client):
    response = api_client.post("/api/forms/contact/", {"email": "bad"}, format="json")

    assert response.status_code == 400
    assert "name" in response.json()


@pytest.mark.django_db
def test_career_form_create(api_client):
    payload = {
        "full_name": "John Smith",
        "address": "123 Main St",
        "contact_number": "9876543210",
        "email": "john@example.com",
        "qualifications": "B.E.",
    }

    response = api_client.post("/api/forms/career/", payload, format="json")

    assert response.status_code == 201
    assert JobApplication.objects.count() == 1


@pytest.mark.django_db
def test_form_endpoints_reject_get(api_client):
    assert api_client.get("/api/forms/contact/").status_code == 405
    assert api_client.get("/api/forms/career/").status_code == 405
