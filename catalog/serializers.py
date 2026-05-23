from rest_framework import serializers

from catalog.models import Machinery, Product, ProductCategory
from core.api.fields import build_absolute_media_url


class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ["id", "name", "slug", "order"]


class ProductSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    category_slug = serializers.CharField(source="category.slug", read_only=True)
    category_name = serializers.CharField(source="category.name", read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "slug",
            "category_slug",
            "category_name",
            "image_url",
            "description",
            "customer",
            "specification",
            "extra_details",
            "order",
        ]

    def get_image_url(self, obj):
        return build_absolute_media_url(self.context.get("request"), obj.image)


class MachinerySerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    plant_display = serializers.CharField(source="get_plant_display", read_only=True)

    class Meta:
        model = Machinery
        fields = [
            "id",
            "name",
            "plant",
            "plant_display",
            "image_url",
            "total_machines",
            "make",
            "year_of_purchase",
            "tonnage_or_capacity",
            "platen_size_or_dimensions",
            "order",
        ]

    def get_image_url(self, obj):
        return build_absolute_media_url(self.context.get("request"), obj.image)
