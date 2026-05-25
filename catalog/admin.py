from django.contrib import admin

from catalog.models import Machinery, Product, ProductCategory


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "order", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name", "slug")
    ordering = ("order", "name")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "slug", "customer", "image", "order", "is_active")
    list_filter = ("is_active", "category")
    search_fields = ("name", "slug", "customer", "description", "category__name")
    ordering = ("order", "name")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Machinery)
class MachineryAdmin(admin.ModelAdmin):
    list_display = ("name", "plant", "total_machines", "make", "image", "order", "is_active")
    list_filter = ("is_active", "plant")
    search_fields = ("name", "make", "tonnage_or_capacity", "platen_size_or_dimensions")
    ordering = ("order", "name")
