from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from rest_framework.views import APIView

from pages.models import WebsitePage
from pages.page_compose import build_page_sections, get_page_banners


class PageDetailView(APIView):
    @extend_schema(
        responses={
            200: {
                "type": "object",
                "properties": {
                    "slug": {"type": "string"},
                    "title": {"type": "string"},
                    "sections": {"type": "array"},
                },
            }
        }
    )
    def get(self, request, slug):
        page = WebsitePage.objects.filter(slug=slug, is_active=True).first()
        if page is None:
            return Response({"detail": "Not found."}, status=404)

        payload = {
            "slug": page.slug,
            "title": page.title,
            "banners": get_page_banners(page, request),
            "sections": build_page_sections(slug, request),
        }
        if page.meta_title:
            payload["meta_title"] = page.meta_title
        if page.meta_description:
            payload["meta_description"] = page.meta_description
        if not payload["banners"]:
            del payload["banners"]
        if not payload["sections"]:
            payload["sections"] = []

        return Response(payload)
