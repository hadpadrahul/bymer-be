from django.contrib import admin

from dashboard.models import AdminAuditEntry, MediaAsset


@admin.register(MediaAsset)
class MediaAssetAdmin(admin.ModelAdmin):
    list_display = ("original_name", "uploaded_by", "uploaded_at")
    readonly_fields = ("uploaded_at",)


@admin.register(AdminAuditEntry)
class AdminAuditEntryAdmin(admin.ModelAdmin):
    list_display = ("action", "model_name", "object_id", "user", "created_at")
    list_filter = ("action", "model_name", "created_at")
    search_fields = ("model_name", "object_id", "message", "user__username")
    readonly_fields = ("created_at",)
    ordering = ("-created_at",)
