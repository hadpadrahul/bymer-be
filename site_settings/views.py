from drf_spectacular.utils import extend_schema
from rest_framework import mixins, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from core.api.mixins import ActiveQuerysetMixin
from site_settings.models import (
    CompanyProfile,
    CompanyStatistic,
    SiteMediaBanner,
    SocialLink,
)
from site_settings.serializers import (
    CompanyProfileSerializer,
    CompanyStatisticSerializer,
    SiteMediaBannerSerializer,
    SocialLinkSerializer,
)


class CompanyProfileAPIView(APIView):
    @extend_schema(responses=CompanyProfileSerializer)
    def get(self, request):
        profile = CompanyProfile.objects.first()
        if profile is None:
            return Response({"detail": "Not found."}, status=404)
        serializer = CompanyProfileSerializer(profile, context={"request": request})
        return Response(serializer.data)


class SocialLinkViewSet(ActiveQuerysetMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = SocialLink.objects.all()
    serializer_class = SocialLinkSerializer


class CompanyStatisticViewSet(
    ActiveQuerysetMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = CompanyStatistic.objects.all()
    serializer_class = CompanyStatisticSerializer


class SiteMediaBannerViewSet(
    ActiveQuerysetMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = SiteMediaBanner.objects.select_related("page")
    serializer_class = SiteMediaBannerSerializer
