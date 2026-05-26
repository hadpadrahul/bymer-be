from dataclasses import dataclass

from catalog.models import Machinery, Product, ProductCategory
from content.models import (
    Award,
    Certification,
    ClientPartner,
    FAQ,
    TeamMember,
    TestimonialDocument,
    TimelineEvent,
)
from site_settings.models import CompanyStatistic, SiteMediaBanner, SocialLink


@dataclass(frozen=True)
class RegistryEntry:
    key: str
    label: str
    model: type
    list_display: tuple[str, ...]
    search_fields: tuple[str, ...]
    public_api_path: str
    nav_group: str
    supports_order: bool = True
    supports_active: bool = True
    list_filter: tuple[str, ...] = ()


REGISTRY: dict[str, RegistryEntry] = {}


def _register(entry: RegistryEntry):
    REGISTRY[entry.key] = entry


_register(
    RegistryEntry(
        key="social-links",
        label="Social links",
        model=SocialLink,
        list_display=("platform", "url", "order", "is_active"),
        search_fields=("platform", "url"),
        public_api_path="/api/globals/social-links/",
        nav_group="Globals",
    )
)
_register(
    RegistryEntry(
        key="statistics",
        label="Statistics",
        model=CompanyStatistic,
        list_display=("label", "value", "order", "is_active"),
        search_fields=("label", "value"),
        public_api_path="/api/globals/statistics/",
        nav_group="Globals",
    )
)
_register(
    RegistryEntry(
        key="banners",
        label="Banners",
        model=SiteMediaBanner,
        list_display=("title", "page", "order", "is_active"),
        search_fields=("title", "subtitle"),
        public_api_path="/api/globals/banners/",
        nav_group="Globals",
    )
)
_register(
    RegistryEntry(
        key="team",
        label="Team members",
        model=TeamMember,
        list_display=("full_name", "designation", "order", "is_active"),
        search_fields=("full_name", "designation"),
        public_api_path="/api/content/team/",
        nav_group="Content",
    )
)
_register(
    RegistryEntry(
        key="timelines",
        label="Timeline",
        model=TimelineEvent,
        list_display=("year", "title", "order", "is_active"),
        search_fields=("year", "title", "description"),
        public_api_path="/api/content/timelines/",
        nav_group="Content",
    )
)
_register(
    RegistryEntry(
        key="clients",
        label="Clients",
        model=ClientPartner,
        list_display=("name", "order", "is_active"),
        search_fields=("name",),
        public_api_path="/api/content/clients/",
        nav_group="Content",
    )
)
_register(
    RegistryEntry(
        key="testimonials",
        label="Testimonials",
        model=TestimonialDocument,
        list_display=("client_or_supplier_name", "document_type", "order", "is_active"),
        search_fields=("client_or_supplier_name",),
        public_api_path="/api/content/testimonials/",
        nav_group="Content",
    )
)
_register(
    RegistryEntry(
        key="certifications",
        label="Certifications",
        model=Certification,
        list_display=("title", "order", "is_active"),
        search_fields=("title",),
        public_api_path="/api/content/certifications/",
        nav_group="Content",
    )
)
_register(
    RegistryEntry(
        key="awards",
        label="Awards",
        model=Award,
        list_display=("title", "order", "is_active"),
        search_fields=("title",),
        public_api_path="/api/content/awards/",
        nav_group="Content",
    )
)
_register(
    RegistryEntry(
        key="faqs",
        label="FAQs",
        model=FAQ,
        list_display=("question", "order", "is_active"),
        search_fields=("question", "answer"),
        public_api_path="/api/content/faqs/",
        nav_group="Content",
    )
)
_register(
    RegistryEntry(
        key="categories",
        label="Product categories",
        model=ProductCategory,
        list_display=("name", "slug", "order", "is_active"),
        search_fields=("name", "slug"),
        public_api_path="/api/catalog/categories/",
        nav_group="Catalog",
    )
)
_register(
    RegistryEntry(
        key="products",
        label="Products",
        model=Product,
        list_display=("name", "category", "order", "is_active"),
        search_fields=("name", "slug", "customer"),
        public_api_path="/api/catalog/products/",
        nav_group="Catalog",
        list_filter=("category", "is_active"),
    )
)
_register(
    RegistryEntry(
        key="machinery",
        label="Machinery",
        model=Machinery,
        list_display=("name", "plant", "order", "is_active"),
        search_fields=("name", "make"),
        public_api_path="/api/catalog/machinery/",
        nav_group="Catalog",
        list_filter=("plant", "is_active"),
    )
)


def get_entry(key: str) -> RegistryEntry:
    if key not in REGISTRY:
        raise KeyError(key)
    return REGISTRY[key]


def nav_groups():
    groups: dict[str, list[RegistryEntry]] = {}
    for entry in REGISTRY.values():
        groups.setdefault(entry.nav_group, []).append(entry)
    return groups
