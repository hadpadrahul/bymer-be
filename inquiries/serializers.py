from rest_framework import serializers

from inquiries.models import ContactInquiry, JobApplication


class ContactInquiryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactInquiry
        fields = ["name", "email", "phone", "subject", "message", "source_page"]

    def create(self, validated_data):
        return ContactInquiry.objects.create(
            status=ContactInquiry.Status.NEW,
            **validated_data,
        )


class JobApplicationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobApplication
        fields = [
            "full_name",
            "date_of_birth",
            "address",
            "city",
            "contact_number",
            "email",
            "qualifications",
            "experience",
            "area_of_interest",
            "expected_ctc",
            "preferred_contact_datetime",
        ]

    def create(self, validated_data):
        return JobApplication.objects.create(
            status=JobApplication.Status.NEW,
            **validated_data,
        )
