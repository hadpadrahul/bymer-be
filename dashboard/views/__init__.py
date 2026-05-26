from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy

from dashboard.views.misc import DashboardHomeView

__all__ = ["DashboardLoginView", "DashboardLogoutView", "DashboardHomeView"]


class DashboardLoginView(LoginView):
    template_name = "dashboard/login.html"
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy("dashboard:home")


class DashboardLogoutView(LogoutView):
    next_page = reverse_lazy("dashboard:login")
