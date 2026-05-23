import pytest

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
def test_repeatable_content_string_representations():
    team_member = TeamMember.objects.create(
        full_name="Rahul Patel",
        designation="Director",
    )
    timeline_event = TimelineEvent.objects.create(
        year="2024",
        title="New Facility",
        description="Expanded manufacturing capacity.",
    )
    client_partner = ClientPartner.objects.create(name="Acme Motors")
    testimonial = DocumentModel.objects.create(client_or_supplier_name="Acme Motors")
    certification = Certification.objects.create(title="ISO 9001")
    award = Award.objects.create(title="Quality Excellence")
    faq = FAQ.objects.create(question="Do you make custom parts?", answer="Yes.")

    assert str(team_member) == "Rahul Patel"
    assert str(timeline_event) == "2024 - New Facility"
    assert str(client_partner) == "Acme Motors"
    assert str(testimonial) == "Acme Motors"
    assert str(certification) == "ISO 9001"
    assert str(award) == "Quality Excellence"
    assert str(faq) == "Do you make custom parts?"


@pytest.mark.django_db
@pytest.mark.parametrize(
    ("model", "kwargs"),
    [
        (TeamMember, {"full_name": "A", "designation": "D"}),
        (TimelineEvent, {"year": "2024", "title": "T", "description": "D"}),
        (ClientPartner, {"name": "Client"}),
        (DocumentModel, {"client_or_supplier_name": "Client"}),
        (Certification, {"title": "Certificate"}),
        (Award, {"title": "Award"}),
        (FAQ, {"question": "Question?", "answer": "Answer."}),
    ],
)
def test_repeatable_content_order_and_active_defaults(model, kwargs):
    instance = model.objects.create(**kwargs)

    assert instance.order == 0
    assert instance.is_active is True


@pytest.mark.django_db
def test_repeatable_content_ordering_uses_order_field():
    second = FAQ.objects.create(question="Second?", answer="B", order=2)
    first = FAQ.objects.create(question="First?", answer="A", order=1)

    assert list(FAQ.objects.all()) == [first, second]


@pytest.mark.django_db
def test_team_member_has_management_pillar_flag():
    member = TeamMember.objects.create(
        full_name="Rahul Patel",
        designation="Director",
        is_management_pillar=True,
    )

    assert member.is_management_pillar is True


@pytest.mark.django_db
def test_testimonial_document_has_document_type():
    testimonial = DocumentModel.objects.create(
        client_or_supplier_name="Acme Motors",
        document_type=DocumentModel.DocumentType.SUPPLIER,
    )

    assert testimonial.document_type == DocumentModel.DocumentType.SUPPLIER
