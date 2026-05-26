from django.urls import path

from dashboard.api.views import AdminHealthView, ToggleActiveView, UpdateOrderView

urlpatterns = [
    path("health/", AdminHealthView.as_view(), name="admin-health"),
    path("<str:registry_key>/<int:pk>/toggle-active/", ToggleActiveView.as_view(), name="toggle-active"),
    path("<str:registry_key>/<int:pk>/order/", UpdateOrderView.as_view(), name="update-order"),
]
