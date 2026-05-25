import pytest
from rest_framework.test import APIClient

from catalog.models import Machinery, Product, ProductCategory


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def automotive_category(db):
    return ProductCategory.objects.create(name="Automotive", slug="automotive")


@pytest.mark.django_db
def test_products_filter_by_category_slug(api_client, automotive_category):
    Product.objects.create(
        category=automotive_category,
        name="Gasket",
        slug="gasket",
        description="Rubber gasket",
    )
    other = ProductCategory.objects.create(name="Other", slug="other")
    Product.objects.create(category=other, name="Widget", slug="widget", description="Other")

    response = api_client.get("/api/catalog/products/?category=automotive")

    assert response.status_code == 200
    assert len(response.json()["results"]) == 1
    assert response.json()["results"][0]["slug"] == "gasket"


@pytest.mark.django_db
def test_machinery_filter_by_plant(api_client):
    Machinery.objects.create(plant=Machinery.Plant.PLANT_1, name="Press 1")
    Machinery.objects.create(plant=Machinery.Plant.PLANT_2, name="Press 2")

    response = api_client.get("/api/catalog/machinery/?plant=plant_1")

    assert response.status_code == 200
    assert len(response.json()["results"]) == 1
    assert response.json()["results"][0]["name"] == "Press 1"


@pytest.mark.django_db
def test_catalog_lists_exclude_inactive(api_client, automotive_category):
    Product.objects.create(
        category=automotive_category,
        name="Hidden",
        slug="hidden",
        description="Hidden",
        is_active=False,
    )

    response = api_client.get("/api/catalog/products/")

    assert response.status_code == 200
    assert response.json()["results"] == []
