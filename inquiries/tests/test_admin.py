import pytest
from django.contrib import admin

from inquiries.admin import ContactInquiryAdmin, JobApplicationAdmin
from inquiries.models import ContactInquiry, JobApplication


@pytest.mark.django_db
def test_inquiry_models_are_registered_in_admin():
    assert isinstance(admin.site._registry[ContactInquiry], ContactInquiryAdmin)
    assert isinstance(admin.site._registry[JobApplication], JobApplicationAdmin)


@pytest.mark.parametrize(
    "admin_class",
    [ContactInquiryAdmin, JobApplicationAdmin],
)
def test_inquiry_admin_classes_expose_review_configuration(admin_class):
    assert admin_class.list_display
    assert admin_class.list_filter
    assert admin_class.search_fields
    assert "created_at" in admin_class.readonly_fields
