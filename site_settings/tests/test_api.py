import pytest
from rest_framework.test import APIClient

from site_settings.models import CompanyProfile, CompanyStatistic, SocialLink


@pytest.fixture
def api_client():
    return APIClient()


@pytest.mark.django_db
def test_company_profile_retrieve(api_client):
    CompanyProfile.objects.create(
        company_name="Bymer",
        email="info@example.com",
        phone="1234567890",
        address="Ahmedabad",
    )

    response = api_client.get("/api/globals/company-profile/")

    assert response.status_code == 200
    assert response.json()["company_name"] == "Bymer"
    assert "email" in response.json()


@pytest.mark.django_db
def test_company_profile_missing_returns_404(api_client):
    response = api_client.get("/api/globals/company-profile/")
    assert response.status_code == 404


@pytest.mark.django_db
def test_social_links_list_active_only(api_client):
    SocialLink.objects.create(platform="LinkedIn", url="https://linkedin.com", order=1)
    SocialLink.objects.create(
        platform="Hidden",
        url="https://hidden.com",
        order=2,
        is_active=False,
    )

    response = api_client.get("/api/globals/social-links/")

    assert response.status_code == 200
    results = response.json()["results"]
    assert len(results) == 1
    assert results[0]["platform"] == "LinkedIn"


@pytest.mark.django_db
def test_statistics_list_smoke(api_client):
    CompanyStatistic.objects.create(label="Years", value="25+")

    response = api_client.get("/api/globals/statistics/")

    assert response.status_code == 200
    assert len(response.json()["results"]) == 1
    assert response.json()["results"][0]["label"] == "Years"
