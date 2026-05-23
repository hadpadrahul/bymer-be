import pytest

from inquiries.models import ContactInquiry, JobApplication


@pytest.mark.django_db
def test_contact_inquiry_defaults_and_string_representation():
    inquiry = ContactInquiry.objects.create(
        name="Jane Doe",
        email="jane@example.com",
        message="Interested in your products.",
        source_page="contact",
    )

    assert str(inquiry) == "Jane Doe (jane@example.com)"
    assert inquiry.status == ContactInquiry.Status.NEW
    assert inquiry.created_at is not None


@pytest.mark.django_db
def test_job_application_defaults_and_string_representation():
    application = JobApplication.objects.create(
        full_name="John Smith",
        address="123 Main Street",
        contact_number="9876543210",
        email="john@example.com",
        qualifications="B.E. Mechanical",
    )

    assert str(application) == "John Smith (john@example.com)"
    assert application.status == JobApplication.Status.NEW
    assert application.created_at is not None
    assert not hasattr(application, "resume_file")


@pytest.mark.django_db
def test_job_application_optional_fields():
    application = JobApplication.objects.create(
        full_name="John Smith",
        date_of_birth="1995-05-01",
        address="123 Main Street",
        city="Ahmedabad",
        contact_number="9876543210",
        email="john@example.com",
        qualifications="B.E. Mechanical",
        experience="5 years in manufacturing",
        area_of_interest="Production",
        expected_ctc="8 LPA",
        preferred_contact_datetime="Weekdays after 5 PM",
    )

    assert application.city == "Ahmedabad"
    assert application.experience == "5 years in manufacturing"
