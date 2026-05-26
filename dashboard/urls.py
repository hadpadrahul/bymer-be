from django.urls import path

from dashboard.views import DashboardLoginView, DashboardLogoutView
from dashboard.views.crud import (
    RegistryCreateView,
    RegistryListView,
    RegistryUpdateView,
    deactivate_registry_item,
)
from dashboard.views.globals import CompanyProfileUpdateView
from dashboard.views.inquiries import InquiryDetailView, InquiryListView, export_inquiries_csv
from dashboard.views.media import MediaLibraryView, MediaUploadView
from dashboard.views.misc import ApiReferenceView, AuditLogListView, DashboardHomeView
from dashboard.views.pages import PageCreateView, PageDetailView, PageListView, PageUpdateView

app_name = "dashboard"

urlpatterns = [
    path("login/", DashboardLoginView.as_view(), name="login"),
    path("logout/", DashboardLogoutView.as_view(), name="logout"),
    path("", DashboardHomeView.as_view(), name="home"),
    path("api-reference/", ApiReferenceView.as_view(), name="api-reference"),
    path("audit-log/", AuditLogListView.as_view(), name="audit-log"),
    path("globals/profile/", CompanyProfileUpdateView.as_view(), name="company-profile"),
    path("pages/", PageListView.as_view(), name="page-list"),
    path("pages/add/", PageCreateView.as_view(), name="page-add"),
    path("pages/<slug:slug>/", PageDetailView.as_view(), name="page-detail"),
    path("pages/<slug:slug>/edit/", PageUpdateView.as_view(), name="page-edit"),
    path("inquiries/<str:inquiry_type>/", InquiryListView.as_view(), name="inquiry-list"),
    path(
        "inquiries/<str:inquiry_type>/<int:pk>/",
        InquiryDetailView.as_view(),
        name="inquiry-detail",
    ),
    path(
        "inquiries/<str:inquiry_type>/export.csv",
        export_inquiries_csv,
        name="inquiry-export",
    ),
    path("media/", MediaLibraryView.as_view(), name="media"),
    path("media/upload/", MediaUploadView.as_view(), name="media-upload"),
    path("manage/<str:registry_key>/", RegistryListView.as_view(), name="list"),
    path("manage/<str:registry_key>/add/", RegistryCreateView.as_view(), name="add"),
    path("manage/<str:registry_key>/<int:pk>/", RegistryUpdateView.as_view(), name="edit"),
    path(
        "manage/<str:registry_key>/<int:pk>/deactivate/",
        deactivate_registry_item,
        name="deactivate",
    ),
]
