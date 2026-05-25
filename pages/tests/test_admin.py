import pytest
from django.contrib import admin

from pages.admin import WebsitePageAdmin
from pages.models import WebsitePage


@pytest.mark.django_db
def test_website_page_is_registered_in_admin():
    assert isinstance(admin.site._registry[WebsitePage], WebsitePageAdmin)


def test_website_page_admin_exposes_editor_fields():
    assert WebsitePageAdmin.list_display
    assert WebsitePageAdmin.search_fields
    assert WebsitePageAdmin.list_filter
    assert WebsitePageAdmin.prepopulated_fields == {"slug": ("title",)}
