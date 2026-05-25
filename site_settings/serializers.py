from rest_framework import serializers

from core.api.fields import build_absolute_media_url
from site_settings.models import (
    CompanyProfile,
    CompanyStatistic,
    SiteMediaBanner,
    SocialLink,
)


class CompanyProfileSerializer(serializers.ModelSerializer):
    logo_url = serializers.SerializerMethodField()

    class Meta:
        model = CompanyProfile
        fields = [
            "company_name",
            "tagline",
            "logo_url",
            "email",
            "phone",
            "alternate_phone",
            "address",
            "website",
        ]

    def get_logo_url(self, obj):
        return build_absolute_media_url(self.context.get("request"), obj.logo)


class SocialLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialLink
        fields = ["id", "platform", "url", "order"]


class CompanyStatisticSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyStatistic
        fields = ["id", "label", "value", "order"]


class SiteMediaBannerSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    page_slug = serializers.CharField(source="page.slug", read_only=True, allow_null=True)

    class Meta:
        model = SiteMediaBanner
        fields = [
            "id",
            "page_slug",
            "title",
            "subtitle",
            "image_url",
            "video_url",
            "order",
        ]

    def get_image_url(self, obj):
        return build_absolute_media_url(self.context.get("request"), obj.image)
