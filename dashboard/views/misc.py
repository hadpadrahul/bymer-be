from django.views.generic import TemplateView

from dashboard.mixins import StaffRequiredMixin
from dashboard.registry import nav_groups
from dashboard.services.health_checks import collect_health_warnings, dashboard_counts
from inquiries.models import ContactInquiry, JobApplication


class DashboardHomeView(StaffRequiredMixin, TemplateView):
    template_name = "dashboard/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["counts"] = dashboard_counts()
        context["warnings"] = collect_health_warnings()
        context["recent_contacts"] = ContactInquiry.objects.all()[:5]
        context["recent_careers"] = JobApplication.objects.all()[:5]
        return context


class ApiReferenceView(StaffRequiredMixin, TemplateView):
    template_name = "dashboard/api_reference.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["endpoints"] = [
            ("/api/health/", "Health"),
            ("/api/globals/company-profile/", "Company profile"),
            ("/api/globals/social-links/", "Social links"),
            ("/api/globals/statistics/", "Statistics"),
            ("/api/globals/banners/", "Banners"),
            ("/api/content/team/", "Team"),
            ("/api/content/timelines/", "Timelines"),
            ("/api/content/clients/", "Clients"),
            ("/api/content/testimonials/", "Testimonials"),
            ("/api/content/certifications/", "Certifications"),
            ("/api/content/awards/", "Awards"),
            ("/api/content/faqs/", "FAQs"),
            ("/api/catalog/categories/", "Categories"),
            ("/api/catalog/products/", "Products"),
            ("/api/catalog/machinery/", "Machinery"),
            ("/api/pages/<slug>/", "Page composition"),
            ("/api/forms/contact/", "Contact form (POST)"),
            ("/api/forms/career/", "Career form (POST)"),
        ]
        return context


class AuditLogListView(StaffRequiredMixin, TemplateView):
    template_name = "dashboard/audit_list.html"

    def get_context_data(self, **kwargs):
        from dashboard.models import AdminAuditEntry

        context = super().get_context_data(**kwargs)
        context["entries"] = AdminAuditEntry.objects.select_related("user")[:100]
        return context
