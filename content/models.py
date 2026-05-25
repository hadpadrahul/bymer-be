from django.db import models


class OrderedActiveModel(models.Model):
    order = models.PositiveIntegerField(default=0, db_index=True)
    is_active = models.BooleanField(default=True, db_index=True)

    class Meta:
        abstract = True
        ordering = ["order", "id"]


class TeamMember(OrderedActiveModel):
    photo = models.ImageField(upload_to="team/", blank=True)
    full_name = models.CharField(max_length=150)
    designation = models.CharField(max_length=150)
    bio = models.TextField(blank=True)
    is_management_pillar = models.BooleanField(default=False, db_index=True)

    def __str__(self):
        return self.full_name


class TimelineEvent(OrderedActiveModel):
    year = models.CharField(max_length=50)
    title = models.CharField(max_length=150)
    description = models.TextField()

    def __str__(self):
        return f"{self.year} - {self.title}"


class ClientPartner(OrderedActiveModel):
    logo = models.ImageField(upload_to="clients/", blank=True)
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name


class TestimonialDocument(OrderedActiveModel):
    class DocumentType(models.TextChoices):
        CUSTOMER = "customer", "Customer"
        SUPPLIER = "supplier", "Supplier"
        OTHER = "other", "Other"

    document = models.FileField(upload_to="documents/testimonials/", blank=True)
    image = models.ImageField(upload_to="documents/testimonials/", blank=True)
    client_or_supplier_name = models.CharField(max_length=150)
    document_type = models.CharField(
        max_length=20,
        choices=DocumentType.choices,
        default=DocumentType.CUSTOMER,
        db_index=True,
    )

    def __str__(self):
        return self.client_or_supplier_name


class Certification(OrderedActiveModel):
    title = models.CharField(max_length=150)
    document = models.FileField(upload_to="documents/certifications/", blank=True)
    image = models.ImageField(upload_to="documents/certifications/", blank=True)

    def __str__(self):
        return self.title


class Award(OrderedActiveModel):
    title = models.CharField(max_length=150)
    document = models.FileField(upload_to="documents/awards/", blank=True)
    image = models.ImageField(upload_to="documents/awards/", blank=True)

    def __str__(self):
        return self.title


class FAQ(OrderedActiveModel):
    question = models.CharField(max_length=255)
    answer = models.TextField()

    class Meta(OrderedActiveModel.Meta):
        verbose_name = "FAQ"
        verbose_name_plural = "FAQs"

    def __str__(self):
        return self.question
