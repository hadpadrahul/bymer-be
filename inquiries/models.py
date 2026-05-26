from django.db import models


class ContactInquiry(models.Model):
    class Status(models.TextChoices):
        NEW = "new", "New"
        REVIEWED = "reviewed", "Reviewed"
        CLOSED = "closed", "Closed"

    name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=50, blank=True)
    subject = models.CharField(max_length=255, blank=True)
    message = models.TextField()
    source_page = models.CharField(max_length=255, blank=True)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.NEW,
        db_index=True,
    )
    internal_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Contact inquiry"
        verbose_name_plural = "Contact inquiries"

    def __str__(self):
        return f"{self.name} ({self.email})"


class JobApplication(models.Model):
    class Status(models.TextChoices):
        NEW = "new", "New"
        REVIEWED = "reviewed", "Reviewed"
        CLOSED = "closed", "Closed"

    full_name = models.CharField(max_length=150)
    date_of_birth = models.DateField(blank=True, null=True)
    address = models.TextField()
    city = models.CharField(max_length=100, blank=True)
    contact_number = models.CharField(max_length=50)
    email = models.EmailField()
    qualifications = models.TextField()
    experience = models.TextField(blank=True)
    area_of_interest = models.CharField(max_length=255, blank=True)
    expected_ctc = models.CharField(max_length=100, blank=True)
    preferred_contact_datetime = models.CharField(max_length=255, blank=True)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.NEW,
        db_index=True,
    )
    internal_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Job application"
        verbose_name_plural = "Job applications"

    def __str__(self):
        return f"{self.full_name} ({self.email})"
