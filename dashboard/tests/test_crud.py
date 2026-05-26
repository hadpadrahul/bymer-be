import pytest
from django.contrib.auth import get_user_model
from django.core import mail
from django.urls import reverse
from rest_framework.test import APIClient

from catalog.models import Product, ProductCategory
from content.models import TeamMember
from dashboard.models import AdminAuditEntry


@pytest.fixture
def staff_user(db):
    User = get_user_model()
    return User.objects.create_user(username="staff", password="pass", is_staff=True)


@pytest.fixture
def staff_client(client, staff_user):
    client.login(username=staff_user.username, password="pass")
    return client


@pytest.mark.django_db
def test_registry_list_accessible(staff_client):
    response = staff_client.get(reverse("dashboard:list", kwargs={"registry_key": "team"}))
    assert response.status_code == 200


@pytest.mark.django_db
def test_company_profile_form(staff_client):
    response = staff_client.get(reverse("dashboard:company-profile"))
    assert response.status_code == 200


@pytest.mark.django_db
def test_toggle_active_api(staff_user):
    member = TeamMember.objects.create(full_name="A", designation="B", order=1, is_active=True)
    api = APIClient()
    api.force_authenticate(user=staff_user)
    response = api.patch(f"/api/admin/team/{member.pk}/toggle-active/")
    assert response.status_code == 200
    member.refresh_from_db()
    assert member.is_active is False


@pytest.mark.django_db
def test_category_delete_blocked_with_products(staff_client):
    category = ProductCategory.objects.create(name="Cat", slug="cat", order=1, is_active=True)
    Product.objects.create(
        name="P",
        slug="p",
        category=category,
        order=1,
        is_active=True,
    )
    response = staff_client.get(
        reverse("dashboard:deactivate", kwargs={"registry_key": "categories", "pk": category.pk})
    )
    assert response.status_code == 302
    assert ProductCategory.objects.filter(pk=category.pk).exists()


@pytest.mark.django_db
def test_inquiry_csv_export(staff_client):
    response = staff_client.get(reverse("dashboard:inquiry-export", kwargs={"inquiry_type": "contact"}))
    assert response.status_code == 200
    assert "text/csv" in response["Content-Type"]


@pytest.mark.django_db
def test_contact_form_sends_email(settings):
    settings.ADMIN_NOTIFICATION_EMAILS = ["admin@example.com"]
    User = get_user_model()
    User.objects.create_user(username="staff", password="pass", is_staff=True)
    client = APIClient()
    response = client.post(
        "/api/forms/contact/",
        {
            "name": "Test",
            "email": "t@example.com",
            "phone": "1",
            "subject": "Hi",
            "message": "Hello",
        },
        format="json",
    )
    assert response.status_code == 201
    assert len(mail.outbox) == 1


@pytest.mark.django_db
def test_audit_logged_on_registry_create(staff_client):
    before = AdminAuditEntry.objects.count()
    response = staff_client.post(
        reverse("dashboard:add", kwargs={"registry_key": "faqs"}),
        {
            "question": "Q?",
            "answer": "A.",
            "order": 1,
            "is_active": True,
        },
    )
    assert response.status_code in (302, 200)
    assert AdminAuditEntry.objects.count() > before
