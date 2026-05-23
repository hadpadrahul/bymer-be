import pytest
from django.core.exceptions import ValidationError

from site_settings.models import CompanyProfile, CompanyStatistic, SocialLink


@pytest.mark.django_db
def test_company_profile_is_singleton():
    CompanyProfile.objects.create(
        company_name="Bymer",
        email="info@example.com",
        phone="1234567890",
        address="Ahmedabad",
    )

    with pytest.raises(ValidationError):
        CompanyProfile.objects.create(
            company_name="Another Bymer",
            email="team@example.com",
            phone="0987654321",
            address="Vadodara",
        )


@pytest.mark.django_db
def test_global_models_string_representations():
    profile = CompanyProfile.objects.create(
        company_name="Bymer Elastomers",
        email="info@example.com",
        phone="1234567890",
        address="Ahmedabad",
    )
    social_link = SocialLink.objects.create(platform="LinkedIn", url="https://example.com")
    statistic = CompanyStatistic.objects.create(label="Years Experience", value="25+")

    assert str(profile) == "Bymer Elastomers"
    assert str(social_link) == "LinkedIn"
    assert str(statistic) == "25+ Years Experience"


@pytest.mark.django_db
def test_repeatable_global_models_have_order_and_active_defaults():
    social_link = SocialLink.objects.create(platform="Website", url="https://example.com")
    statistic = CompanyStatistic.objects.create(label="Clients", value="100+")

    assert social_link.order == 0
    assert social_link.is_active is True
    assert statistic.order == 0
    assert statistic.is_active is True
