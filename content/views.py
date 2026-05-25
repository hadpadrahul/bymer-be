from rest_framework import mixins, viewsets

from content.filters import TeamMemberFilter, TestimonialDocumentFilter
from content.models import (
    Award,
    Certification,
    ClientPartner,
    FAQ,
    TeamMember,
    TestimonialDocument,
    TimelineEvent,
)
from content.serializers import (
    AwardSerializer,
    CertificationSerializer,
    ClientPartnerSerializer,
    FAQSerializer,
    TeamMemberSerializer,
    TestimonialDocumentSerializer,
    TimelineEventSerializer,
)
from core.api.mixins import ActiveQuerysetMixin


class ReadOnlyListViewSet(ActiveQuerysetMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    pass


class TeamMemberViewSet(ReadOnlyListViewSet):
    queryset = TeamMember.objects.all()
    serializer_class = TeamMemberSerializer
    filterset_class = TeamMemberFilter


class TimelineEventViewSet(ReadOnlyListViewSet):
    queryset = TimelineEvent.objects.all()
    serializer_class = TimelineEventSerializer


class ClientPartnerViewSet(ReadOnlyListViewSet):
    queryset = ClientPartner.objects.all()
    serializer_class = ClientPartnerSerializer


class TestimonialDocumentViewSet(ReadOnlyListViewSet):
    queryset = TestimonialDocument.objects.all()
    serializer_class = TestimonialDocumentSerializer
    filterset_class = TestimonialDocumentFilter


class CertificationViewSet(ReadOnlyListViewSet):
    queryset = Certification.objects.all()
    serializer_class = CertificationSerializer


class AwardViewSet(ReadOnlyListViewSet):
    queryset = Award.objects.all()
    serializer_class = AwardSerializer


class FAQViewSet(ReadOnlyListViewSet):
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer
