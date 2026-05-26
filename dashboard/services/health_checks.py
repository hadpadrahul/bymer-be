from catalog.models import Product, ProductCategory
from content.models import TeamMember
from inquiries.models import ContactInquiry, JobApplication
from pages.models import WebsitePage
from site_settings.models import SiteMediaBanner


def collect_health_warnings():
    warnings = []

    for member in TeamMember.objects.filter(is_active=True, photo=""):
        warnings.append(
            {"level": "warning", "message": f"Team member missing photo: {member.full_name}", "kind": "missing_image"}
        )

    for product in Product.objects.filter(is_active=True, image=""):
        warnings.append(
            {"level": "warning", "message": f"Product missing image: {product.name}", "kind": "missing_image"}
        )

    for page in WebsitePage.objects.filter(is_active=False):
        if SiteMediaBanner.objects.filter(page=page, is_active=True).exists():
            warnings.append(
                {
                    "level": "warning",
                    "message": f"Inactive page has active banner: {page.slug}",
                    "kind": "inactive_page_banner",
                }
            )

    for category in ProductCategory.objects.filter(is_active=True):
        if not Product.objects.filter(category=category, is_active=True).exists():
            warnings.append(
                {
                    "level": "info",
                    "message": f"Category has no active products: {category.name}",
                    "kind": "empty_category",
                }
            )

    inactive_count = (
        TeamMember.objects.filter(is_active=False).count()
        + Product.objects.filter(is_active=False).count()
    )
    if inactive_count:
        warnings.append(
            {
                "level": "info",
                "message": f"{inactive_count} inactive content record(s) on site",
                "kind": "inactive_content",
            }
        )

    return warnings


def dashboard_counts():
    return {
        "contact_new": ContactInquiry.objects.filter(status=ContactInquiry.Status.NEW).count(),
        "career_new": JobApplication.objects.filter(status=JobApplication.Status.NEW).count(),
        "products": Product.objects.filter(is_active=True).count(),
        "pages": WebsitePage.objects.filter(is_active=True).count(),
    }
