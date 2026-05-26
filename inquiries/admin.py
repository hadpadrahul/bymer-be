from django.contrib import admin

from inquiries.models import ContactInquiry, JobApplication


@admin.register(ContactInquiry)
class ContactInquiryAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone", "subject", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("name", "email", "phone", "subject", "message", "source_page")
    readonly_fields = ("created_at",)
    ordering = ("-created_at",)
    fields = (
        "name",
        "email",
        "phone",
        "subject",
        "message",
        "source_page",
        "status",
        "internal_notes",
        "created_at",
    )


@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ("full_name", "email", "contact_number", "city", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = (
        "full_name",
        "email",
        "contact_number",
        "city",
        "qualifications",
        "experience",
        "area_of_interest",
    )
    readonly_fields = ("created_at",)
    ordering = ("-created_at",)
    fields = (
        "full_name",
        "date_of_birth",
        "address",
        "city",
        "contact_number",
        "email",
        "qualifications",
        "experience",
        "area_of_interest",
        "expected_ctc",
        "preferred_contact_datetime",
        "status",
        "internal_notes",
        "created_at",
    )
