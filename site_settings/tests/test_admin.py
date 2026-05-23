import pytest
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.test import RequestFactory

from site_settings.admin import (
    CompanyProfileAdmin,
    CompanyStatisticAdmin,
    SiteMediaBannerAdmin,
    SocialLinkAdmin,
)
from site_settings.models import (
    CompanyProfile,
    CompanyStatistic,
    SiteMediaBanner,
    SocialLink,
)


@pytest.mark.django_db
def test_site_settings_models_are_registered_in_admin():
    assert isinstance(admin.site._registry[CompanyProfile], CompanyProfileAdmin)
    assert isinstance(admin.site._registry[SocialLink], SocialLinkAdmin)
    assert isinstance(admin.site._registry[CompanyStatistic], CompanyStatisticAdmin)
    assert isinstance(admin.site._registry[SiteMediaBanner], SiteMediaBannerAdmin)


def test_site_settings_admin_classes_expose_editor_fields():
    assert CompanyProfileAdmin.list_display
    assert CompanyProfileAdmin.search_fields
    assert SocialLinkAdmin.list_display
    assert SocialLinkAdmin.search_fields
    assert SocialLinkAdmin.list_filter
    assert CompanyStatisticAdmin.list_display
    assert CompanyStatisticAdmin.search_fields
    assert CompanyStatisticAdmin.list_filter
    assert SiteMediaBannerAdmin.list_display
    assert SiteMediaBannerAdmin.search_fields
    assert SiteMediaBannerAdmin.list_filter


@pytest.mark.django_db
def test_company_profile_admin_cannot_add_second_profile():
    CompanyProfile.objects.create(
        company_name="Bymer",
        email="info@example.com",
        phone="1234567890",
        address="Ahmedabad",
    )
    request = RequestFactory().get("/admin/site_settings/companyprofile/add/")
    request.user = get_user_model().objects.create_superuser(
        username="admin",
        email="admin@example.com",
        password="password",
    )
    model_admin = admin.site._registry[CompanyProfile]

    assert model_admin.has_add_permission(request) is False
