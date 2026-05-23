from django.core.exceptions import ValidationError
from django.db import models


class CompanyProfile(models.Model):
    company_name = models.CharField(max_length=255)
    tagline = models.CharField(max_length=255, blank=True)
    logo = models.ImageField(upload_to="company/", blank=True)
    email = models.EmailField()
    phone = models.CharField(max_length=50)
    alternate_phone = models.CharField(max_length=50, blank=True)
    address = models.TextField()
    website = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Company profile"
        verbose_name_plural = "Company profile"

    def __str__(self):
        return self.company_name

    def clean(self):
        if CompanyProfile.objects.exclude(pk=self.pk).exists():
            raise ValidationError("Only one company profile can exist.")

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)


class SocialLink(models.Model):
    platform = models.CharField(max_length=100)
    url = models.URLField()
    order = models.PositiveIntegerField(default=0, db_index=True)
    is_active = models.BooleanField(default=True, db_index=True)

    class Meta:
        ordering = ["order", "platform"]

    def __str__(self):
        return self.platform


class CompanyStatistic(models.Model):
    label = models.CharField(max_length=150)
    value = models.CharField(max_length=100)
    order = models.PositiveIntegerField(default=0, db_index=True)
    is_active = models.BooleanField(default=True, db_index=True)

    class Meta:
        ordering = ["order", "label"]

    def __str__(self):
        return f"{self.value} {self.label}"


class SiteMediaBanner(models.Model):
    page = models.ForeignKey(
        "pages.WebsitePage",
        on_delete=models.CASCADE,
        related_name="banners",
        blank=True,
        null=True,
    )
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255, blank=True)
    image = models.ImageField(upload_to="banners/", blank=True)
    video_url = models.URLField(blank=True)
    order = models.PositiveIntegerField(default=0, db_index=True)
    is_active = models.BooleanField(default=True, db_index=True)

    class Meta:
        ordering = ["order", "title"]

    def __str__(self):
        return self.title
