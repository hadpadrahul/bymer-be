import pytest
from django.db import IntegrityError

from pages.models import WebsitePage


@pytest.mark.django_db
def test_website_page_string_defaults_and_slug_uniqueness():
    page = WebsitePage.objects.create(title="About Us", slug="about-us")

    assert str(page) == "About Us"
    assert page.is_active is True
    assert page.order == 0

    with pytest.raises(IntegrityError):
        WebsitePage.objects.create(title="About Again", slug="about-us")


@pytest.mark.django_db
def test_website_page_ordering():
    second = WebsitePage.objects.create(title="Second", slug="second", order=2)
    first = WebsitePage.objects.create(title="First", slug="first", order=1)

    assert list(WebsitePage.objects.all()) == [first, second]
