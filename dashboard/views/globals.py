from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import UpdateView

from dashboard.audit import log_audit
from dashboard.forms import CompanyProfileForm
from dashboard.mixins import StaffRequiredMixin
from site_settings.models import CompanyProfile


class CompanyProfileUpdateView(StaffRequiredMixin, UpdateView):
    model = CompanyProfile
    form_class = CompanyProfileForm
    template_name = "dashboard/model_form.html"
    success_url = reverse_lazy("dashboard:company-profile")

    def get_object(self, queryset=None):
        profile = CompanyProfile.objects.first()
        if profile is None:
            profile = CompanyProfile.objects.create(
                company_name="Company name",
                email="info@example.com",
                phone="0000000000",
                address="Address pending",
            )
        return profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["entry"] = type(
            "Entry",
            (),
            {
                "label": "Company profile",
                "key": "company-profile",
                "public_api_path": "/api/globals/company-profile/",
            },
        )()
        context["is_create"] = False
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        log_audit(self.request, action="update", model_name="CompanyProfile", object_id=self.object.pk)
        messages.success(self.request, "Company profile saved.")
        return response
