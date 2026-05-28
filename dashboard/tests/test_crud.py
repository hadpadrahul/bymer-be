import pytest
from django.contrib.auth import get_user_model
from django.core import mail
from django.urls import reverse
from rest_framework.test import APIClient

from catalog.models import Product, ProductCategory
from content.models import TeamMember
from dashboard.models import AdminAuditEntry
from inquiries.models import ContactInquiry


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
def test_inquiry_csv_export_respects_filters_and_selection(staff_client):
    first = ContactInquiry.objects.create(
        name="A",
        email="a@example.com",
        phone="123",
        subject="s1",
        message="m1",
        status=ContactInquiry.Status.NEW,
    )
    ContactInquiry.objects.create(
        name="B",
        email="b@example.com",
        phone="456",
        subject="s2",
        message="m2",
        status=ContactInquiry.Status.CLOSED,
    )
    filtered = staff_client.get(
        reverse("dashboard:inquiry-export", kwargs={"inquiry_type": "contact"}),
        {"status": ContactInquiry.Status.NEW},
    )
    assert filtered.status_code == 200
    assert "a@example.com" in filtered.content.decode("utf-8")
    assert "b@example.com" not in filtered.content.decode("utf-8")

    selected = staff_client.get(
        reverse("dashboard:inquiry-export", kwargs={"inquiry_type": "contact"}),
        {"selected_ids": [first.pk]},
    )
    assert selected.status_code == 200
    assert "a@example.com" in selected.content.decode("utf-8")


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


@pytest.mark.django_db
def test_bulk_deactivate_registry_items(staff_client):
    first = TeamMember.objects.create(full_name="One", designation="Role", order=1, is_active=True)
    second = TeamMember.objects.create(full_name="Two", designation="Role", order=2, is_active=True)
    response = staff_client.post(
        reverse("dashboard:bulk-deactivate", kwargs={"registry_key": "team"}),
        {"selected_ids": [first.pk, second.pk]},
    )
    assert response.status_code == 302
    first.refresh_from_db()
    second.refresh_from_db()
    assert first.is_active is False
    assert second.is_active is False
