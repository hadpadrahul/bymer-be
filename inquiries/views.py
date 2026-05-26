from drf_spectacular.utils import extend_schema
from rest_framework import generics, status
from rest_framework.response import Response

from dashboard.services.notifications import notify_contact_inquiry, notify_job_application
from inquiries.models import ContactInquiry, JobApplication
from inquiries.serializers import ContactInquiryCreateSerializer, JobApplicationCreateSerializer


class ContactInquiryCreateView(generics.CreateAPIView):
    queryset = ContactInquiry.objects.all()
    serializer_class = ContactInquiryCreateSerializer

    @extend_schema(request=ContactInquiryCreateSerializer, responses={201: dict})
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        inquiry = serializer.save()
        notify_contact_inquiry(inquiry)
        return Response({"success": True}, status=status.HTTP_201_CREATED)


class JobApplicationCreateView(generics.CreateAPIView):
    queryset = JobApplication.objects.all()
    serializer_class = JobApplicationCreateSerializer

    @extend_schema(request=JobApplicationCreateSerializer, responses={201: dict})
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        application = serializer.save()
        notify_job_application(application)
        return Response({"success": True}, status=status.HTTP_201_CREATED)
