from rest_framework import serializers

from content.models import (
    Award,
    Certification,
    ClientPartner,
    FAQ,
    TeamMember,
    TestimonialDocument,
    TimelineEvent,
)
from core.api.fields import build_absolute_media_url


class TeamMemberSerializer(serializers.ModelSerializer):
    photo_url = serializers.SerializerMethodField()

    class Meta:
        model = TeamMember
        fields = [
            "id",
            "full_name",
            "designation",
            "bio",
            "is_management_pillar",
            "photo_url",
            "order",
        ]

    def get_photo_url(self, obj):
        return build_absolute_media_url(self.context.get("request"), obj.photo)


class TimelineEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimelineEvent
        fields = ["id", "year", "title", "description", "order"]


class ClientPartnerSerializer(serializers.ModelSerializer):
    logo_url = serializers.SerializerMethodField()

    class Meta:
        model = ClientPartner
        fields = ["id", "name", "logo_url", "order"]

    def get_logo_url(self, obj):
        return build_absolute_media_url(self.context.get("request"), obj.logo)


class TestimonialDocumentSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    document_url = serializers.SerializerMethodField()

    class Meta:
        model = TestimonialDocument
        fields = [
            "id",
            "client_or_supplier_name",
            "document_type",
            "image_url",
            "document_url",
            "order",
        ]

    def get_image_url(self, obj):
        return build_absolute_media_url(self.context.get("request"), obj.image)

    def get_document_url(self, obj):
        return build_absolute_media_url(self.context.get("request"), obj.document)


class CertificationSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    document_url = serializers.SerializerMethodField()

    class Meta:
        model = Certification
        fields = ["id", "title", "image_url", "document_url", "order"]

    def get_image_url(self, obj):
        return build_absolute_media_url(self.context.get("request"), obj.image)

    def get_document_url(self, obj):
        return build_absolute_media_url(self.context.get("request"), obj.document)


class AwardSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    document_url = serializers.SerializerMethodField()

    class Meta:
        model = Award
        fields = ["id", "title", "image_url", "document_url", "order"]

    def get_image_url(self, obj):
        return build_absolute_media_url(self.context.get("request"), obj.image)

    def get_document_url(self, obj):
        return build_absolute_media_url(self.context.get("request"), obj.document)


class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = ["id", "question", "answer", "order"]
