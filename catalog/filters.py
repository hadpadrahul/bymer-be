import django_filters

from catalog.models import Machinery, Product


class ProductFilter(django_filters.FilterSet):
    category = django_filters.CharFilter(field_name="category__slug")

    class Meta:
        model = Product
        fields = ["category"]


class MachineryFilter(django_filters.FilterSet):
    plant = django_filters.ChoiceFilter(choices=Machinery.Plant.choices)

    class Meta:
        model = Machinery
        fields = ["plant"]
