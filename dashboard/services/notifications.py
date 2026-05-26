from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse


def notify_admins_new_submission(*, subject: str, body: str):
    recipients = getattr(settings, "ADMIN_NOTIFICATION_EMAILS", None) or []
    if not recipients:
        return
    send_mail(
        subject=subject,
        message=body,
        from_email=None,
        recipient_list=recipients,
        fail_silently=True,
    )


def notify_contact_inquiry(inquiry):
    path = reverse("dashboard:inquiry-detail", kwargs={"inquiry_type": "contact", "pk": inquiry.pk})
    body = (
        f"New contact inquiry from {inquiry.name} ({inquiry.email})\n"
        f"Phone: {inquiry.phone}\n"
        f"Subject: {inquiry.subject}\n\n"
        f"Review in dashboard: {path}\n"
    )
    notify_admins_new_submission(subject=f"[Bymer] Contact: {inquiry.subject or inquiry.name}", body=body)


def notify_job_application(application):
    path = reverse("dashboard:inquiry-detail", kwargs={"inquiry_type": "career", "pk": application.pk})
    body = (
        f"New career application from {application.full_name} ({application.email})\n"
        f"Phone: {application.contact_number}\n\n"
        f"Review in dashboard: {path}\n"
    )
    notify_admins_new_submission(
        subject=f"[Bymer] Career application: {application.full_name}",
        body=body,
    )
