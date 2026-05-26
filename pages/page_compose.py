from django.db.models import Q

from catalog.models import Product
from catalog.serializers import MachinerySerializer, ProductSerializer
from content.models import (
    Award,
    Certification,
    FAQ,
    TeamMember,
    TestimonialDocument,
    TimelineEvent,
)
from content.serializers import (
    AwardSerializer,
    CertificationSerializer,
    FAQSerializer,
    TeamMemberSerializer,
    TestimonialDocumentSerializer,
    TimelineEventSerializer,
)
from site_settings.models import CompanyStatistic, SiteMediaBanner
from site_settings.serializers import CompanyStatisticSerializer, SiteMediaBannerSerializer


PAGE_SECTION_MAP = {
    "home": ["statistics"],
    "our-team": ["team"],
    "our-history": ["timelines"],
    "testimonials": ["testimonials"],
    "quality-assurance": ["certifications", "awards"],
    "automotive-products": ["products"],
    "non-automotive-products": ["products"],
    "machinery": ["machinery"],
    "contact-us": ["faqs"],
}

SECTION_COLLECTION_LINKS = {
    "statistics": ("dashboard:list", "statistics"),
    "team": ("dashboard:list", "team"),
    "timelines": ("dashboard:list", "timelines"),
    "testimonials": ("dashboard:list", "testimonials"),
    "certifications": ("dashboard:list", "certifications"),
    "awards": ("dashboard:list", "awards"),
    "faqs": ("dashboard:list", "faqs"),
    "products": ("dashboard:list", "products"),
    "machinery": ("dashboard:list", "machinery"),
}


def get_known_page_slugs():
    return list(PAGE_SECTION_MAP.keys())


def _serialize(queryset, serializer_class, request):
    return serializer_class(queryset, many=True, context={"request": request}).data


def _section(section_type, queryset, serializer_class, request):
    data = _serialize(queryset, serializer_class, request)
    if not data:
        return None
    return {"type": section_type, "data": data}


def build_page_sections(slug, request):
    sections = []

    if slug == "home":
        stats = CompanyStatistic.objects.filter(is_active=True)
        section = _section("statistics", stats, CompanyStatisticSerializer, request)
        if section:
            sections.append(section)

    elif slug == "our-team":
        team = TeamMember.objects.filter(is_active=True)
        section = _section("team", team, TeamMemberSerializer, request)
        if section:
            sections.append(section)

    elif slug == "our-history":
        timelines = TimelineEvent.objects.filter(is_active=True)
        section = _section("timelines", timelines, TimelineEventSerializer, request)
        if section:
            sections.append(section)

    elif slug == "testimonials":
        testimonials = TestimonialDocument.objects.filter(is_active=True)
        section = _section("testimonials", testimonials, TestimonialDocumentSerializer, request)
        if section:
            sections.append(section)

    elif slug == "quality-assurance":
        certifications = Certification.objects.filter(is_active=True)
        awards = Award.objects.filter(is_active=True)
        for section_type, queryset, serializer in (
            ("certifications", certifications, CertificationSerializer),
            ("awards", awards, AwardSerializer),
        ):
            section = _section(section_type, queryset, serializer, request)
            if section:
                sections.append(section)

    elif slug in ("automotive-products", "non-automotive-products"):
        products = Product.objects.filter(is_active=True, category__slug=slug).select_related(
            "category"
        )
        section = _section("products", products, ProductSerializer, request)
        if section:
            sections.append(section)

    elif slug == "machinery":
        from catalog.models import Machinery

        machinery = Machinery.objects.filter(is_active=True)
        section = _section("machinery", machinery, MachinerySerializer, request)
        if section:
            sections.append(section)

    elif slug == "contact-us":
        faqs = FAQ.objects.filter(is_active=True)
        section = _section("faqs", faqs, FAQSerializer, request)
        if section:
            sections.append(section)

    return sections


def get_page_banners(page, request):
    banners = (
        SiteMediaBanner.objects.filter(is_active=True)
        .filter(Q(page=page) | Q(page__isnull=True))
        .select_related("page")
        .order_by("order", "title")
    )
    return SiteMediaBannerSerializer(banners, many=True, context={"request": request}).data
