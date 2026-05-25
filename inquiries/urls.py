from django.urls import path

from inquiries.views import ContactInquiryCreateView, JobApplicationCreateView

urlpatterns = [
    path("contact/", ContactInquiryCreateView.as_view(), name="contact-create"),
    path("career/", JobApplicationCreateView.as_view(), name="career-create"),
]
