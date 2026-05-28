from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Q
from django.db.models.fields.related import ForeignKey
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import CreateView, ListView, UpdateView

from catalog.models import ProductCategory
from dashboard.audit import log_audit
from dashboard.forms import get_form_class
from dashboard.mixins import StaffRequiredMixin
from dashboard.registry import get_entry


class RegistryListView(StaffRequiredMixin, ListView):
    template_name = "dashboard/model_list.html"
    context_object_name = "items"
    paginate_by = 25

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.registry_key = kwargs["registry_key"]
        self.entry = get_entry(self.registry_key)

    def get_queryset(self):
        qs = self.entry.model.objects.all()
        relation_fields = []
        for column in self.entry.list_display:
            try:
                field = self.entry.model._meta.get_field(column)
            except Exception:
                continue
            if isinstance(field, ForeignKey):
                relation_fields.append(column)
        if relation_fields:
            qs = qs.select_related(*relation_fields)
        search = self.request.GET.get("q", "").strip()
        if search and self.entry.search_fields:
            query = Q()
            for field in self.entry.search_fields:
                query |= Q(**{f"{field}__icontains": search})
            qs = qs.filter(query)
        active = self.request.GET.get("active")
        if active == "1" and self.entry.supports_active:
            qs = qs.filter(is_active=True)
        elif active == "0" and self.entry.supports_active:
            qs = qs.filter(is_active=False)
        for field in self.entry.list_filter:
            value = self.request.GET.get(field)
            if value:
                qs = qs.filter(**{field: value})
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["entry"] = self.entry
        context["search_query"] = self.request.GET.get("q", "")
        context["active_filter"] = self.request.GET.get("active", "")
        filters = []
        for field_name in self.entry.list_filter:
            if field_name == "is_active":
                continue
            try:
                field = self.entry.model._meta.get_field(field_name)
            except Exception:
                continue
            if hasattr(field, "related_model") and field.related_model:
                choices = [
                    (str(obj.pk), str(obj))
                    for obj in field.related_model.objects.all()[:200]
                ]
                filters.append(
                    {
                        "name": field_name,
                        "label": field.verbose_name.title(),
                        "choices": choices,
                        "selected": self.request.GET.get(field_name, ""),
                    }
                )
        context["extra_filters"] = filters
        return context


class RegistryCreateView(StaffRequiredMixin, CreateView):
    template_name = "dashboard/model_form.html"

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.registry_key = kwargs["registry_key"]
        self.entry = get_entry(self.registry_key)

    def get_form_class(self):
        return get_form_class(self.registry_key)

    def form_valid(self, form):
        response = super().form_valid(form)
        log_audit(
            self.request,
            action="create",
            model_name=self.entry.model.__name__,
            object_id=self.object.pk,
        )
        messages.success(self.request, f"{self.entry.label} created.")
        return response

    def get_success_url(self):
        return reverse("dashboard:edit", kwargs={"registry_key": self.registry_key, "pk": self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["entry"] = self.entry
        context["is_create"] = True
        return context


class RegistryUpdateView(StaffRequiredMixin, UpdateView):
    template_name = "dashboard/model_form.html"

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.registry_key = kwargs["registry_key"]
        self.entry = get_entry(self.registry_key)

    def get_queryset(self):
        return self.entry.model.objects.all()

    def get_form_class(self):
        return get_form_class(self.registry_key)

    def form_valid(self, form):
        response = super().form_valid(form)
        log_audit(
            self.request,
            action="update",
            model_name=self.entry.model.__name__,
            object_id=self.object.pk,
        )
        messages.success(self.request, f"{self.entry.label} saved.")
        return response

    def get_success_url(self):
        return reverse("dashboard:edit", kwargs={"registry_key": self.registry_key, "pk": self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["entry"] = self.entry
        context["is_create"] = False
        return context


@staff_member_required(login_url="/dashboard/login/")
def deactivate_registry_item(request, registry_key, pk):
    entry = get_entry(registry_key)
    obj = get_object_or_404(entry.model, pk=pk)
    if hasattr(obj, "is_active"):
        obj.is_active = False
        obj.save(update_fields=["is_active"])
        log_audit(request, action="deactivate", model_name=entry.model.__name__, object_id=pk)
        messages.success(request, f"{entry.label} deactivated.")
    else:
        if registry_key == "categories" and obj.products.exists():
            messages.error(request, "Cannot delete category with products.")
            return redirect("dashboard:list", registry_key=registry_key)
        obj.delete()
        log_audit(request, action="delete", model_name=entry.model.__name__, object_id=pk)
        messages.success(request, f"{entry.label} removed.")
    return redirect("dashboard:list", registry_key=registry_key)
