from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic import FormView, ListView

from dashboard.audit import log_audit
from dashboard.forms import MediaUploadForm
from dashboard.mixins import StaffRequiredMixin
from dashboard.models import MediaAsset


class MediaLibraryView(StaffRequiredMixin, ListView):
    model = MediaAsset
    template_name = "dashboard/media_library.html"
    context_object_name = "assets"
    paginate_by = 24

    def get_queryset(self):
        return MediaAsset.objects.select_related("uploaded_by").all()


class MediaUploadView(StaffRequiredMixin, FormView):
    form_class = MediaUploadForm
    template_name = "dashboard/media_upload.html"
    success_url = "/dashboard/media/"

    def form_valid(self, form):
        asset = MediaAsset.objects.create(
            file=form.cleaned_data["file"],
            original_name=form.cleaned_data["file"].name,
            uploaded_by=self.request.user,
        )
        log_audit(self.request, action="upload", model_name="MediaAsset", object_id=asset.pk)
        messages.success(self.request, "File uploaded.")
        return redirect(self.success_url)
