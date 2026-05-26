import csv

from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import DetailView, ListView, UpdateView

from dashboard.audit import log_audit
from dashboard.forms import ContactInquiryForm, JobApplicationForm
from dashboard.mixins import StaffRequiredMixin
from inquiries.models import ContactInquiry, JobApplication


class InquiryListView(StaffRequiredMixin, ListView):
    template_name = "dashboard/inquiry_list.html"
    context_object_name = "items"
    paginate_by = 25

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.inquiry_type = kwargs["inquiry_type"]
        self.model = ContactInquiry if self.inquiry_type == "contact" else JobApplication

    def get_queryset(self):
        qs = self.model.objects.all()
        search = self.request.GET.get("q", "").strip()
        if search:
            if self.inquiry_type == "contact":
                qs = qs.filter(
                    Q(name__icontains=search)
                    | Q(email__icontains=search)
                    | Q(phone__icontains=search)
                )
            else:
                qs = qs.filter(
                    Q(full_name__icontains=search)
                    | Q(email__icontains=search)
                    | Q(contact_number__icontains=search)
                )
        status = self.request.GET.get("status")
        if status:
            qs = qs.filter(status=status)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["inquiry_type"] = self.inquiry_type
        context["title"] = "Contact inquiries" if self.inquiry_type == "contact" else "Career applications"
        context["status_choices"] = self.model.Status.choices
        return context


class InquiryDetailView(StaffRequiredMixin, UpdateView):
    template_name = "dashboard/inquiry_detail.html"

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.inquiry_type = kwargs["inquiry_type"]
        self.model = ContactInquiry if self.inquiry_type == "contact" else JobApplication

    def get_queryset(self):
        return self.model.objects.all()

    def get_form_class(self):
        return ContactInquiryForm if self.inquiry_type == "contact" else JobApplicationForm

    def get_success_url(self):
        return reverse(
            "dashboard:inquiry-detail",
            kwargs={"inquiry_type": self.inquiry_type, "pk": self.object.pk},
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["inquiry_type"] = self.inquiry_type
        context["readonly_fields"] = self.object
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        log_audit(
            self.request,
            action="update",
            model_name=self.model.__name__,
            object_id=self.object.pk,
            message="status/notes",
        )
        messages.success(self.request, "Submission updated.")
        return response


@staff_member_required(login_url="/dashboard/login/")
def export_inquiries_csv(request, inquiry_type):
    model = ContactInquiry if inquiry_type == "contact" else JobApplication
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = f'attachment; filename="{inquiry_type}-submissions.csv"'
    writer = csv.writer(response)
    if inquiry_type == "contact":
        writer.writerow(["name", "email", "phone", "subject", "status", "created_at", "message"])
        for row in model.objects.all():
            writer.writerow(
                [row.name, row.email, row.phone, row.subject, row.status, row.created_at, row.message]
            )
    else:
        writer.writerow(["full_name", "email", "contact_number", "city", "status", "created_at"])
        for row in model.objects.all():
            writer.writerow(
                [row.full_name, row.email, row.contact_number, row.city, row.status, row.created_at]
            )
    return response
