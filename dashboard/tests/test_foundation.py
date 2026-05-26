import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_dashboard_home_requires_staff(client):
    User = get_user_model()
    user = User.objects.create_user(username="staff", password="pass", is_staff=True)
    client.login(username="staff", password="pass")
    response = client.get(reverse("dashboard:home"))
    assert response.status_code == 200


@pytest.mark.django_db
def test_dashboard_home_redirects_anonymous(client):
    response = client.get(reverse("dashboard:home"))
    assert response.status_code == 302
    assert "/dashboard/login/" in response.url


@pytest.mark.django_db
def test_non_staff_cannot_access_dashboard(client):
    User = get_user_model()
    User.objects.create_user(username="user", password="pass", is_staff=False)
    client.login(username="user", password="pass")
    response = client.get(reverse("dashboard:home"))
    assert response.status_code == 403


@pytest.mark.django_db
def test_admin_api_health_requires_staff():
    User = get_user_model()
    staff = User.objects.create_user(username="staff", password="pass", is_staff=True)
    api = APIClient()
    api.force_authenticate(user=staff)
    response = api.get("/api/admin/health/")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


@pytest.mark.django_db
def test_admin_api_health_denies_anonymous():
    api = APIClient()
    response = api.get("/api/admin/health/")
    assert response.status_code in (401, 403)
