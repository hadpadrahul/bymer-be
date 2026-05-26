from django.conf import settings
from django.contrib import messages
from django.db.models import Q
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from dashboard.audit import log_audit
from dashboard.forms import WebsitePageForm
from dashboard.mixins import StaffRequiredMixin
from pages.models import WebsitePage
from pages.page_compose import PAGE_SECTION_MAP, SECTION_COLLECTION_LINKS, build_page_sections


class PageListView(StaffRequiredMixin, ListView):
    model = WebsitePage
    template_name = "dashboard/page_list.html"
    context_object_name = "pages"
    paginate_by = 25

    def get_queryset(self):
        qs = WebsitePage.objects.all()
        search = self.request.GET.get("q", "").strip()
        if search:
            qs = qs.filter(Q(title__icontains=search) | Q(slug__icontains=search))
        return qs


class PageCreateView(StaffRequiredMixin, CreateView):
    model = WebsitePage
    form_class = WebsitePageForm
    template_name = "dashboard/model_form.html"
    success_url = reverse_lazy("dashboard:page-list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["entry"] = type(
            "Entry",
            (),
            {"label": "Page", "key": "pages", "public_api_path": "/api/pages/{slug}/"},
        )()
        context["is_create"] = True
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        log_audit(self.request, action="create", model_name="WebsitePage", object_id=self.object.pk)
        messages.success(self.request, "Page created.")
        return response


class PageUpdateView(StaffRequiredMixin, UpdateView):
    model = WebsitePage
    form_class = WebsitePageForm
    template_name = "dashboard/model_form.html"

    def get_success_url(self):
        return reverse("dashboard:page-detail", kwargs={"slug": self.object.slug})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["entry"] = type(
            "Entry",
            (),
            {
                "label": "Page",
                "key": "pages",
                "public_api_path": f"/api/pages/{self.object.slug}/",
            },
        )()
        context["is_create"] = False
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        log_audit(self.request, action="update", model_name="WebsitePage", object_id=self.object.pk)
        messages.success(self.request, "Page saved.")
        return response


class PageDetailView(StaffRequiredMixin, DetailView):
    model = WebsitePage
    template_name = "dashboard/page_detail.html"
    context_object_name = "page"
    slug_url_kwarg = "slug"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page = self.object
        section_types = PAGE_SECTION_MAP.get(page.slug, [])
        sections = []
        for section_type in section_types:
            link = SECTION_COLLECTION_LINKS.get(section_type)
            sections.append({"type": section_type, "manage_url": reverse(link[0], args=link[1:]) if link else None})
        context["section_rows"] = sections
        context["public_api_path"] = f"/api/pages/{page.slug}/"
        base = getattr(settings, "PUBLIC_WEBSITE_BASE_URL", "").rstrip("/")
        context["preview_url"] = f"{base}/{page.slug}/" if base else ""
        return context
