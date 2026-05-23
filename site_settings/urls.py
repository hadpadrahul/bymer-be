from django.urls import path
from rest_framework.routers import DefaultRouter

from site_settings.views import (
    CompanyProfileAPIView,
    CompanyStatisticViewSet,
    SiteMediaBannerViewSet,
    SocialLinkViewSet,
)

router = DefaultRouter()
router.register("social-links", SocialLinkViewSet, basename="social-link")
router.register("statistics", CompanyStatisticViewSet, basename="statistic")
router.register("banners", SiteMediaBannerViewSet, basename="banner")

urlpatterns = [
    path("company-profile/", CompanyProfileAPIView.as_view(), name="company-profile"),
    *router.urls,
]
