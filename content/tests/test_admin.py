import pytest
from django.contrib import admin

from content.admin import (
    AwardAdmin,
    CertificationAdmin,
    ClientPartnerAdmin,
    FAQAdmin,
    TeamMemberAdmin,
    TestimonialDocumentAdmin as DocumentAdmin,
    TimelineEventAdmin,
)
from content.models import (
    Award,
    Certification,
    ClientPartner,
    FAQ,
    TeamMember,
    TestimonialDocument as DocumentModel,
    TimelineEvent,
)


@pytest.mark.django_db
def test_content_models_are_registered_in_admin():
    assert isinstance(admin.site._registry[TeamMember], TeamMemberAdmin)
    assert isinstance(admin.site._registry[TimelineEvent], TimelineEventAdmin)
    assert isinstance(admin.site._registry[ClientPartner], ClientPartnerAdmin)
    assert isinstance(admin.site._registry[DocumentModel], DocumentAdmin)
    assert isinstance(admin.site._registry[Certification], CertificationAdmin)
    assert isinstance(admin.site._registry[Award], AwardAdmin)
    assert isinstance(admin.site._registry[FAQ], FAQAdmin)


@pytest.mark.parametrize(
    "admin_class",
    [
        TeamMemberAdmin,
        TimelineEventAdmin,
        ClientPartnerAdmin,
        DocumentAdmin,
        CertificationAdmin,
        AwardAdmin,
        FAQAdmin,
    ],
)
def test_content_admin_classes_expose_editor_configuration(admin_class):
    assert admin_class.list_display
    assert admin_class.search_fields
    assert admin_class.list_filter
