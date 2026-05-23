import pytest
from django.db import IntegrityError

from catalog.models import Machinery, Product, ProductCategory


@pytest.mark.django_db
def test_product_category_string_defaults_and_slug_uniqueness():
    category = ProductCategory.objects.create(name="Automotive", slug="automotive")

    assert str(category) == "Automotive"
    assert category.order == 0
    assert category.is_active is True

    with pytest.raises(IntegrityError):
        ProductCategory.objects.create(name="Auto Again", slug="automotive")


@pytest.mark.django_db
def test_product_string_defaults_relationship_and_slug_uniqueness():
    category = ProductCategory.objects.create(name="Automotive", slug="automotive")
    product = Product.objects.create(
        category=category,
        name="Rubber Gasket",
        slug="rubber-gasket",
        description="Molded rubber gasket.",
    )

    assert str(product) == "Rubber Gasket"
    assert product.category == category
    assert product.order == 0
    assert product.is_active is True
    assert list(category.products.all()) == [product]

    with pytest.raises(IntegrityError):
        Product.objects.create(
            category=category,
            name="Rubber Gasket Duplicate",
            slug="rubber-gasket",
            description="Duplicate slug.",
        )


@pytest.mark.django_db
def test_catalog_ordering_uses_order_field():
    second = ProductCategory.objects.create(name="Second", slug="second", order=2)
    first = ProductCategory.objects.create(name="First", slug="first", order=1)

    assert list(ProductCategory.objects.all()) == [first, second]


@pytest.mark.django_db
def test_machinery_plant_choices_defaults_and_string_representation():
    machinery = Machinery.objects.create(
        plant=Machinery.Plant.PLANT_1,
        name="Injection Molding Machine",
        total_machines=4,
    )

    assert str(machinery) == "Injection Molding Machine"
    assert machinery.plant == Machinery.Plant.PLANT_1
    assert machinery.get_plant_display() == "Plant I"
    assert machinery.order == 0
    assert machinery.is_active is True
