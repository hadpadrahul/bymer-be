from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from dashboard.mixins import StaffRequiredMixin


class DashboardLoginView(LoginView):
    template_name = "dashboard/login.html"
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy("dashboard:home")


class DashboardLogoutView(LogoutView):
    next_page = reverse_lazy("dashboard:login")


class DashboardHomeView(StaffRequiredMixin, TemplateView):
    template_name = "dashboard/home.html"
