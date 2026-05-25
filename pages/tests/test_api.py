import pytest
from rest_framework.test import APIClient

from content.models import TeamMember
from pages.models import WebsitePage


@pytest.fixture
def api_client():
    return APIClient()


@pytest.mark.django_db
def test_page_detail_returns_sections(api_client):
    WebsitePage.objects.create(title="Our Team", slug="our-team")
    TeamMember.objects.create(full_name="Jane Doe", designation="Director")

    response = api_client.get("/api/pages/our-team/")

    assert response.status_code == 200
    data = response.json()
    assert data["slug"] == "our-team"
    assert data["title"] == "Our Team"
    assert any(section["type"] == "team" for section in data["sections"])


@pytest.mark.django_db
def test_page_detail_unknown_slug_404(api_client):
    response = api_client.get("/api/pages/missing-page/")
    assert response.status_code == 404


@pytest.mark.django_db
def test_page_detail_inactive_404(api_client):
    WebsitePage.objects.create(title="Hidden", slug="hidden", is_active=False)

    response = api_client.get("/api/pages/hidden/")

    assert response.status_code == 404


@pytest.mark.django_db
def test_page_omits_blank_meta_fields(api_client):
    WebsitePage.objects.create(title="About", slug="about-us")

    response = api_client.get("/api/pages/about-us/")

    assert response.status_code == 200
    data = response.json()
    assert "meta_title" not in data
    assert "meta_description" not in data
