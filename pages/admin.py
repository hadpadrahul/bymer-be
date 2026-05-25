from django.contrib import admin

from pages.models import WebsitePage


@admin.register(WebsitePage)
class WebsitePageAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "order", "is_active", "updated_at")
    list_filter = ("is_active",)
    search_fields = ("title", "slug", "meta_title", "meta_description")
    ordering = ("order", "title")
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ("created_at", "updated_at")
