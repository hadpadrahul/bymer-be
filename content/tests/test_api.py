import pytest
from rest_framework.test import APIClient

from content.models import TeamMember, TestimonialDocument


@pytest.fixture
def api_client():
    return APIClient()


@pytest.mark.django_db
def test_team_list_excludes_inactive(api_client):
    TeamMember.objects.create(full_name="Active", designation="Director")
    TeamMember.objects.create(
        full_name="Inactive",
        designation="Hidden",
        is_active=False,
    )

    response = api_client.get("/api/content/team/")

    assert response.status_code == 200
    assert len(response.json()["results"]) == 1
    assert response.json()["results"][0]["full_name"] == "Active"


@pytest.mark.django_db
def test_team_pillar_filter(api_client):
    TeamMember.objects.create(full_name="Leader", designation="CEO", is_management_pillar=True)
    TeamMember.objects.create(full_name="Staff", designation="Engineer", is_management_pillar=False)

    response = api_client.get("/api/content/team/?pillar=true")

    assert response.status_code == 200
    assert len(response.json()["results"]) == 1
    assert response.json()["results"][0]["full_name"] == "Leader"


@pytest.mark.django_db
def test_testimonial_type_filter(api_client):
    TestimonialDocument.objects.create(
        client_or_supplier_name="Customer A",
        document_type=TestimonialDocument.DocumentType.CUSTOMER,
    )
    TestimonialDocument.objects.create(
        client_or_supplier_name="Supplier B",
        document_type=TestimonialDocument.DocumentType.SUPPLIER,
    )

    response = api_client.get("/api/content/testimonials/?type=supplier")

    assert response.status_code == 200
    assert len(response.json()["results"]) == 1
    assert response.json()["results"][0]["client_or_supplier_name"] == "Supplier B"
