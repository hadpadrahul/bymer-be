from django.urls import path

from pages.views import PageDetailView

urlpatterns = [
    path("<slug:slug>/", PageDetailView.as_view(), name="page-detail"),
]
