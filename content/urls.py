from rest_framework.routers import DefaultRouter

from content.views import (
    AwardViewSet,
    CertificationViewSet,
    ClientPartnerViewSet,
    FAQViewSet,
    TeamMemberViewSet,
    TestimonialDocumentViewSet,
    TimelineEventViewSet,
)

router = DefaultRouter()
router.register("team", TeamMemberViewSet, basename="team")
router.register("timelines", TimelineEventViewSet, basename="timeline")
router.register("clients", ClientPartnerViewSet, basename="client")
router.register("testimonials", TestimonialDocumentViewSet, basename="testimonial")
router.register("certifications", CertificationViewSet, basename="certification")
router.register("awards", AwardViewSet, basename="award")
router.register("faqs", FAQViewSet, basename="faq")

urlpatterns = router.urls
