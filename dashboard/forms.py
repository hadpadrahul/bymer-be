from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError

from catalog.models import Machinery, Product, ProductCategory
from content.models import (
    Award,
    Certification,
    ClientPartner,
    FAQ,
    TeamMember,
    TestimonialDocument,
    TimelineEvent,
)
from dashboard.registry import REGISTRY
from inquiries.models import ContactInquiry, JobApplication
from pages.models import WebsitePage
from pages.page_compose import get_known_page_slugs
from site_settings.models import CompanyProfile, CompanyStatistic, SiteMediaBanner, SocialLink


class DashboardModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            css = "w-full rounded border border-slate-300 px-3 py-2 text-sm"
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs["class"] = "rounded border-slate-300"
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs["class"] = f"{css} min-h-[100px]"
            else:
                field.widget.attrs["class"] = css


class CompanyProfileForm(DashboardModelForm):
    class Meta:
        model = CompanyProfile
        fields = [
            "company_name",
            "tagline",
            "logo",
            "email",
            "phone",
            "alternate_phone",
            "address",
            "map_url",
            "gstin",
            "website",
        ]


class SocialLinkForm(DashboardModelForm):
    class Meta:
        model = SocialLink
        fields = ["platform", "url", "order", "is_active"]


class CompanyStatisticForm(DashboardModelForm):
    class Meta:
        model = CompanyStatistic
        fields = ["label", "value", "order", "is_active"]


class SiteMediaBannerForm(DashboardModelForm):
    class Meta:
        model = SiteMediaBanner
        fields = [
            "page",
            "title",
            "subtitle",
            "image",
            "video_url",
            "cta_text",
            "cta_button_url",
            "order",
            "is_active",
        ]


class WebsitePageForm(DashboardModelForm):
    class Meta:
        model = WebsitePage
        fields = ["title", "slug", "meta_title", "meta_description", "order", "is_active"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        known = get_known_page_slugs()
        self.fields["slug"].widget = forms.Select(choices=[(s, s) for s in known])


class TeamMemberForm(DashboardModelForm):
    class Meta:
        model = TeamMember
        fields = [
            "photo",
            "full_name",
            "designation",
            "bio",
            "is_management_pillar",
            "order",
            "is_active",
        ]


class TimelineEventForm(DashboardModelForm):
    class Meta:
        model = TimelineEvent
        fields = ["year", "title", "description", "order", "is_active"]


class ClientPartnerForm(DashboardModelForm):
    class Meta:
        model = ClientPartner
        fields = ["logo", "name", "order", "is_active"]


class TestimonialDocumentForm(DashboardModelForm):
    class Meta:
        model = TestimonialDocument
        fields = [
            "client_or_supplier_name",
            "document_type",
            "image",
            "document",
            "order",
            "is_active",
        ]


class CertificationForm(DashboardModelForm):
    class Meta:
        model = Certification
        fields = ["title", "image", "document", "order", "is_active"]


class AwardForm(DashboardModelForm):
    class Meta:
        model = Award
        fields = ["title", "image", "document", "order", "is_active"]


class FAQForm(DashboardModelForm):
    class Meta:
        model = FAQ
        fields = ["question", "answer", "order", "is_active"]


class ProductCategoryForm(DashboardModelForm):
    class Meta:
        model = ProductCategory
        fields = ["name", "slug", "order", "is_active"]


class ProductForm(DashboardModelForm):
    class Meta:
        model = Product
        fields = [
            "category",
            "name",
            "slug",
            "image",
            "description",
            "customer",
            "specification",
            "extra_details",
            "order",
            "is_active",
        ]


class MachineryForm(DashboardModelForm):
    class Meta:
        model = Machinery
        fields = [
            "plant",
            "name",
            "image",
            "total_machines",
            "make",
            "year_of_purchase",
            "tonnage_or_capacity",
            "platen_size_or_dimensions",
            "order",
            "is_active",
        ]


class ContactInquiryForm(DashboardModelForm):
    class Meta:
        model = ContactInquiry
        fields = ["status", "internal_notes"]


class JobApplicationForm(DashboardModelForm):
    class Meta:
        model = JobApplication
        fields = ["status", "internal_notes"]


class MediaUploadForm(forms.Form):
    file = forms.FileField()

    def clean_file(self):
        uploaded = self.cleaned_data["file"]
        max_mb = getattr(settings, "DASHBOARD_MAX_UPLOAD_MB", 10)
        max_bytes = max_mb * 1024 * 1024
        if uploaded.size > max_bytes:
            raise ValidationError(f"File must be {max_mb} MB or smaller.")
        return uploaded


FORM_MAP = {
    "social-links": SocialLinkForm,
    "statistics": CompanyStatisticForm,
    "banners": SiteMediaBannerForm,
    "team": TeamMemberForm,
    "timelines": TimelineEventForm,
    "clients": ClientPartnerForm,
    "testimonials": TestimonialDocumentForm,
    "certifications": CertificationForm,
    "awards": AwardForm,
    "faqs": FAQForm,
    "categories": ProductCategoryForm,
    "products": ProductForm,
    "machinery": MachineryForm,
}


def get_form_class(registry_key: str):
    return FORM_MAP[registry_key]
