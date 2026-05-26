from django.contrib import admin

from site_settings.models import (
    CompanyProfile,
    CompanyStatistic,
    SiteMediaBanner,
    SocialLink,
)


@admin.register(CompanyProfile)
class CompanyProfileAdmin(admin.ModelAdmin):
    list_display = ("company_name", "email", "phone", "updated_at")
    search_fields = ("company_name", "email", "phone", "address")
    readonly_fields = ("created_at", "updated_at")

    def has_add_permission(self, request):
        return not CompanyProfile.objects.exists() and super().has_add_permission(request)


@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ("platform", "url", "order", "is_active")
    list_filter = ("is_active",)
    search_fields = ("platform", "url")
    ordering = ("order", "platform")


@admin.register(CompanyStatistic)
class CompanyStatisticAdmin(admin.ModelAdmin):
    list_display = ("label", "value", "order", "is_active")
    list_filter = ("is_active",)
    search_fields = ("label", "value")
    ordering = ("order", "label")


@admin.register(SiteMediaBanner)
class SiteMediaBannerAdmin(admin.ModelAdmin):
    list_display = ("title", "page", "order", "is_active", "image", "video_url", "cta_text")
    list_filter = ("is_active", "page")
    search_fields = ("title", "subtitle", "page__title", "page__slug")
    ordering = ("order", "title")
