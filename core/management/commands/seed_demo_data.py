from django.core.management.base import BaseCommand
from django.db import transaction

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
from pathlib import Path

from core.management.demo_media import load_image_from_dir, make_demo_image
from inquiries.models import ContactInquiry, JobApplication
from pages.models import WebsitePage
from site_settings.models import CompanyProfile, CompanyStatistic, SiteMediaBanner, SocialLink


class Command(BaseCommand):
    help = "Seed realistic demo website content for local API testing (optional PNG images)."

    def add_arguments(self, parser):
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Remove previously seeded demo records before seeding.",
        )
        parser.add_argument(
            "--no-images",
            action="store_true",
            help="Seed text-only records without generating image/file uploads.",
        )
        parser.add_argument(
            "--media-dir",
            default="",
            help="Folder with real images named logo, banner, team, client, etc. (see README).",
        )

    def handle(self, *args, **options):
        media_dir = Path(options["media_dir"]).resolve() if options["media_dir"] else None
        with transaction.atomic():
            if options["clear"]:
                self._clear_demo_data()
            with_images = not options["no_images"]
            summary = self._seed_all(with_images=with_images, media_dir=media_dir)

        self.stdout.write(self.style.SUCCESS("Demo data ready."))
        for label, count in summary.items():
            self.stdout.write(f"  {label}: {count}")
        self.stdout.write("")
        if media_dir:
            self.stdout.write(f"  Media folder: {media_dir}")
        self.stdout.write("Next steps:")
        self.stdout.write("  1. python manage.py runserver")
        self.stdout.write("  2. python manage.py benchmark_apis")
        self.stdout.write("  3. python manage.py benchmark_apis --rounds 3  (optional latency median)")

    def _clear_demo_data(self):
        JobApplication.objects.filter(email__endswith="@demo.bymer.local").delete()
        ContactInquiry.objects.filter(email__endswith="@demo.bymer.local").delete()
        Product.objects.filter(slug__startswith="demo-").delete()
        ProductCategory.objects.filter(slug__in=["automotive-products", "non-automotive-products"]).delete()
        Machinery.objects.filter(name__startswith="Demo ").delete()
        TeamMember.objects.filter(full_name__startswith="Demo ").delete()
        TimelineEvent.objects.filter(title__startswith="Demo ").delete()
        ClientPartner.objects.filter(name__startswith="Demo ").delete()
        TestimonialDocument.objects.filter(client_or_supplier_name__startswith="Demo ").delete()
        Certification.objects.filter(title__startswith="Demo ").delete()
        Award.objects.filter(title__startswith="Demo ").delete()
        FAQ.objects.filter(question__startswith="Demo ").delete()
        SiteMediaBanner.objects.filter(title__startswith="Demo ").delete()
        CompanyStatistic.objects.filter(label__startswith="Demo ").delete()
        SocialLink.objects.filter(platform__startswith="Demo ").delete()
        WebsitePage.objects.filter(slug__in=self._page_slugs()).delete()
        CompanyProfile.objects.filter(company_name="Bymer Elastomers (Demo)").delete()
        self.stdout.write(self.style.WARNING("Cleared demo records."))

    def _image_file(self, media_dir: Path | None, basename: str, fallback_name: str, color: tuple[int, int, int]):
        if media_dir:
            loaded = load_image_from_dir(media_dir, basename)
            if loaded:
                return loaded
        return make_demo_image(fallback_name, color)

    def _seed_all(self, *, with_images: bool, media_dir: Path | None = None):
        pages = self._seed_pages()
        profile = self._seed_globals(pages, with_images=with_images, media_dir=media_dir)
        self._seed_content(with_images=with_images, media_dir=media_dir)
        self._seed_catalog(with_images=with_images, media_dir=media_dir)
        self._seed_sample_inquiries()
        return {
            "company_profile": 1 if profile else 0,
            "pages": len(pages),
            "content_models": 7,
            "catalog_models": 3,
            "sample_inquiries": 2,
        }

    def _page_slugs(self):
        return [
            "home",
            "about-us",
            "our-team",
            "our-history",
            "automotive-products",
            "non-automotive-products",
            "machinery",
            "process",
            "testimonials",
            "quality-assurance",
            "contact-us",
            "career-with-us",
        ]

    def _seed_pages(self):
        pages = []
        for index, slug in enumerate(self._page_slugs()):
            page, _ = WebsitePage.objects.update_or_create(
                slug=slug,
                defaults={
                    "title": slug.replace("-", " ").title(),
                    "meta_title": f"Bymer | {slug.replace('-', ' ').title()}",
                    "meta_description": f"Demo description for {slug}.",
                    "order": index,
                    "is_active": True,
                },
            )
            pages.append(page)
        inactive, _ = WebsitePage.objects.update_or_create(
            slug="inactive-demo-page",
            defaults={
                "title": "Inactive Demo Page",
                "order": 99,
                "is_active": False,
            },
        )
        pages.append(inactive)
        return pages

    def _seed_globals(self, pages, *, with_images: bool, media_dir: Path | None = None):
        profile_defaults = {
            "company_name": "Bymer Elastomers (Demo)",
            "tagline": "Quality rubber and polymer solutions",
            "email": "info@demo.bymer.local",
            "phone": "+91 98765 43210",
            "alternate_phone": "+91 98765 43211",
            "address": "Demo Industrial Estate, Ahmedabad, Gujarat, India",
            "website": "https://example.com",
        }
        if CompanyProfile.objects.exists():
            profile = CompanyProfile.objects.first()
            for field, value in profile_defaults.items():
                setattr(profile, field, value)
            if with_images and not profile.logo:
                profile.logo.save(
                    "demo-logo.png",
                    self._image_file(media_dir, "logo", "demo-logo.png", (30, 90, 160)),
                    save=False,
                )
            profile.save()
        else:
            profile = CompanyProfile(**profile_defaults)
            if with_images:
                profile.logo.save(
                    "demo-logo.png",
                    self._image_file(media_dir, "logo", "demo-logo.png", (30, 90, 160)),
                    save=False,
                )
            profile.save()

        SocialLink.objects.update_or_create(
            platform="Demo LinkedIn",
            defaults={"url": "https://linkedin.com/company/bymer-demo", "order": 1, "is_active": True},
        )
        SocialLink.objects.update_or_create(
            platform="Demo Hidden",
            defaults={"url": "https://hidden.example.com", "order": 2, "is_active": False},
        )

        for order, (label, value) in enumerate(
            [
                ("Demo Years of Experience", "25+"),
                ("Demo Clients Served", "120+"),
                ("Demo Products", "450+"),
            ],
            start=1,
        ):
            CompanyStatistic.objects.update_or_create(
                label=label,
                defaults={"value": value, "order": order, "is_active": True},
            )

        home = next((page for page in pages if page.slug == "home"), None)
        banner_defaults = {
            "title": "Demo Home Banner",
            "subtitle": "Engineered for performance",
            "video_url": "",
            "order": 1,
            "is_active": True,
            "page": home,
        }
        banner, created = SiteMediaBanner.objects.get_or_create(title="Demo Home Banner", defaults=banner_defaults)
        if not created:
            for field, value in banner_defaults.items():
                setattr(banner, field, value)
        if with_images and not banner.image:
            banner.image.save(
                "demo-home-banner.png",
                self._image_file(media_dir, "banner", "demo-home-banner.png", (180, 60, 40)),
                save=False,
            )
        banner.save()
        return profile

    def _seed_content(self, *, with_images: bool, media_dir: Path | None = None):
        team, _ = TeamMember.objects.update_or_create(
            full_name="Demo Rahul Patel",
            defaults={
                "designation": "Managing Director",
                "bio": "Leads manufacturing and quality programs.",
                "is_management_pillar": True,
                "order": 1,
                "is_active": True,
            },
        )
        if with_images and not team.photo:
            team.photo.save(
                "demo-team.png",
                self._image_file(media_dir, "team", "demo-team.png", (90, 120, 180)),
                save=False,
            )
            team.save()

        TeamMember.objects.update_or_create(
            full_name="Demo Priya Shah",
            defaults={
                "designation": "Plant Manager",
                "bio": "Oversees daily production operations.",
                "is_management_pillar": False,
                "order": 2,
                "is_active": True,
            },
        )

        TimelineEvent.objects.update_or_create(
            title="Demo Facility Expansion",
            defaults={
                "year": "2022",
                "description": "Expanded Plant II capacity for automotive components.",
                "order": 1,
                "is_active": True,
            },
        )

        client, _ = ClientPartner.objects.update_or_create(
            name="Demo Acme Motors",
            defaults={"order": 1, "is_active": True},
        )
        if with_images and not client.logo:
            client.logo.save(
                "demo-client.png",
                self._image_file(media_dir, "client", "demo-client.png", (200, 80, 80)),
                save=False,
            )
            client.save()

        testimonial, _ = TestimonialDocument.objects.update_or_create(
            client_or_supplier_name="Demo Customer Corp",
            defaults={
                "document_type": TestimonialDocument.DocumentType.CUSTOMER,
                "order": 1,
                "is_active": True,
            },
        )
        if with_images and not testimonial.image:
            testimonial.image.save(
                "demo-testimonial.png",
                self._image_file(media_dir, "testimonial", "demo-testimonial.png", (120, 120, 120)),
                save=False,
            )
            testimonial.save()

        cert, _ = Certification.objects.update_or_create(
            title="Demo ISO 9001",
            defaults={"order": 1, "is_active": True},
        )
        if with_images and not cert.image:
            cert.image.save(
                "demo-cert.png",
                self._image_file(media_dir, "cert", "demo-cert.png", (80, 140, 80)),
                save=False,
            )
            cert.save()

        award, _ = Award.objects.update_or_create(
            title="Demo Quality Excellence",
            defaults={"order": 1, "is_active": True},
        )
        if with_images and not award.image:
            award.image.save(
                "demo-award.png",
                self._image_file(media_dir, "award", "demo-award.png", (140, 100, 60)),
                save=False,
            )
            award.save()

        FAQ.objects.update_or_create(
            question="Demo: Do you support custom rubber compounds?",
            defaults={
                "answer": "Yes. Custom formulations are available for approved applications.",
                "order": 1,
                "is_active": True,
            },
        )

    def _seed_catalog(self, *, with_images: bool, media_dir: Path | None = None):
        auto_category, _ = ProductCategory.objects.update_or_create(
            slug="automotive-products",
            defaults={"name": "Automotive Products", "order": 1, "is_active": True},
        )
        non_auto_category, _ = ProductCategory.objects.update_or_create(
            slug="non-automotive-products",
            defaults={"name": "Non-Automotive Products", "order": 2, "is_active": True},
        )

        for category, slug, name in [
            (auto_category, "demo-brake-seal", "Demo Brake Seal"),
            (auto_category, "demo-engine-mount", "Demo Engine Mount"),
            (non_auto_category, "demo-industrial-gasket", "Demo Industrial Gasket"),
        ]:
            product, _ = Product.objects.update_or_create(
                slug=slug,
                defaults={
                    "category": category,
                    "name": name,
                    "description": f"{name} for demo API testing.",
                    "customer": "Demo OEM",
                    "specification": "Heat resistant compound",
                    "order": 1,
                    "is_active": True,
                },
            )
            if with_images and not product.image:
                product.image.save(
                    f"{slug}.png",
                    self._image_file(media_dir, "product", f"{slug}.png", (100, 150, 200)),
                    save=False,
                )
                product.save()

        for plant, machine_name in [
            (Machinery.Plant.PLANT_1, "Demo Injection Press A"),
            (Machinery.Plant.PLANT_2, "Demo Compression Press B"),
        ]:
            machine, _ = Machinery.objects.update_or_create(
                name=machine_name,
                defaults={
                    "plant": plant,
                    "total_machines": 4,
                    "make": "DemoMake",
                    "year_of_purchase": 2019,
                    "tonnage_or_capacity": "120T",
                    "order": 1,
                    "is_active": True,
                },
            )
            if with_images and not machine.image:
                machine.image.save(
                    f"{machine_name.replace(' ', '-').lower()}.png",
                    self._image_file(media_dir, "machinery", f"{machine_name}.png", (60, 90, 120)),
                    save=False,
                )
                machine.save()

    def _seed_sample_inquiries(self):
        ContactInquiry.objects.get_or_create(
            email="contact@demo.bymer.local",
            defaults={
                "name": "Demo Contact User",
                "phone": "9999999999",
                "subject": "Demo inquiry",
                "message": "Seeded inquiry for admin review.",
                "source_page": "contact-us",
            },
        )
        JobApplication.objects.get_or_create(
            email="career@demo.bymer.local",
            defaults={
                "full_name": "Demo Applicant",
                "address": "Demo Street",
                "city": "Ahmedabad",
                "contact_number": "8888888888",
                "qualifications": "Diploma in Mechanical Engineering",
            },
        )
