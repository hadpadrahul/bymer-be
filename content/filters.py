import django_filters

from content.models import TeamMember, TestimonialDocument


class TeamMemberFilter(django_filters.FilterSet):
    pillar = django_filters.BooleanFilter(field_name="is_management_pillar")

    class Meta:
        model = TeamMember
        fields = ["pillar"]


class TestimonialDocumentFilter(django_filters.FilterSet):
    type = django_filters.ChoiceFilter(field_name="document_type", choices=TestimonialDocument.DocumentType.choices)

    class Meta:
        model = TestimonialDocument
        fields = ["type"]
