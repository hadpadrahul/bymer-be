from django.urls import path

from dashboard.views import DashboardHomeView, DashboardLoginView, DashboardLogoutView

app_name = "dashboard"

urlpatterns = [
    path("login/", DashboardLoginView.as_view(), name="login"),
    path("logout/", DashboardLogoutView.as_view(), name="logout"),
    path("", DashboardHomeView.as_view(), name="home"),
]
