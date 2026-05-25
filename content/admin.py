from django.contrib import admin

from content.models import (
    Award,
    Certification,
    ClientPartner,
    FAQ,
    TeamMember,
    TestimonialDocument,
    TimelineEvent,
)


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ("full_name", "designation", "is_management_pillar", "order", "is_active", "photo")
    list_filter = ("is_active", "is_management_pillar")
    search_fields = ("full_name", "designation", "bio")
    ordering = ("order", "full_name")


@admin.register(TimelineEvent)
class TimelineEventAdmin(admin.ModelAdmin):
    list_display = ("year", "title", "order", "is_active")
    list_filter = ("is_active", "year")
    search_fields = ("year", "title", "description")
    ordering = ("order", "year")


@admin.register(ClientPartner)
class ClientPartnerAdmin(admin.ModelAdmin):
    list_display = ("name", "logo", "order", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name",)
    ordering = ("order", "name")


@admin.register(TestimonialDocument)
class TestimonialDocumentAdmin(admin.ModelAdmin):
    list_display = ("client_or_supplier_name", "document_type", "document", "image", "order", "is_active")
    list_filter = ("is_active", "document_type")
    search_fields = ("client_or_supplier_name",)
    ordering = ("order", "client_or_supplier_name")


@admin.register(Certification)
class CertificationAdmin(admin.ModelAdmin):
    list_display = ("title", "document", "image", "order", "is_active")
    list_filter = ("is_active",)
    search_fields = ("title",)
    ordering = ("order", "title")


@admin.register(Award)
class AwardAdmin(admin.ModelAdmin):
    list_display = ("title", "document", "image", "order", "is_active")
    list_filter = ("is_active",)
    search_fields = ("title",)
    ordering = ("order", "title")


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ("question", "order", "is_active")
    list_filter = ("is_active",)
    search_fields = ("question", "answer")
    ordering = ("order", "question")
