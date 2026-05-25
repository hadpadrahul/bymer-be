import pytest
from django.contrib import admin

from catalog.admin import MachineryAdmin, ProductAdmin, ProductCategoryAdmin
from catalog.models import Machinery, Product, ProductCategory


@pytest.mark.django_db
def test_catalog_models_are_registered_in_admin():
    assert isinstance(admin.site._registry[ProductCategory], ProductCategoryAdmin)
    assert isinstance(admin.site._registry[Product], ProductAdmin)
    assert isinstance(admin.site._registry[Machinery], MachineryAdmin)


@pytest.mark.parametrize(
    "admin_class",
    [ProductCategoryAdmin, ProductAdmin, MachineryAdmin],
)
def test_catalog_admin_classes_expose_editor_configuration(admin_class):
    assert admin_class.list_display
    assert admin_class.search_fields
    assert admin_class.list_filter


def test_catalog_slug_admin_classes_are_prepopulated():
    assert ProductCategoryAdmin.prepopulated_fields == {"slug": ("name",)}
    assert ProductAdmin.prepopulated_fields == {"slug": ("name",)}
