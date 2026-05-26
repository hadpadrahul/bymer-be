from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/globals/", include("site_settings.urls")),
    path("api/content/", include("content.urls")),
    path("api/catalog/", include("catalog.urls")),
    path("api/pages/", include("pages.urls")),
    path("api/forms/", include("inquiries.urls")),
    path("api/", include("core.urls")),
    path("api/admin/", include("dashboard.api.urls")),
    path("dashboard/", include("dashboard.urls")),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
