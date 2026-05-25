from rest_framework import mixins, viewsets

from catalog.filters import MachineryFilter, ProductFilter
from catalog.models import Machinery, Product, ProductCategory
from catalog.serializers import (
    MachinerySerializer,
    ProductCategorySerializer,
    ProductSerializer,
)
from core.api.mixins import ActiveQuerysetMixin


class ProductCategoryViewSet(ActiveQuerysetMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer


class ProductViewSet(ActiveQuerysetMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Product.objects.select_related("category")
    serializer_class = ProductSerializer
    filterset_class = ProductFilter


class MachineryViewSet(ActiveQuerysetMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Machinery.objects.all()
    serializer_class = MachinerySerializer
    filterset_class = MachineryFilter
