from django.conf import settings
from django.db import models


class AdminAuditEntry(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="dashboard_audit_entries",
    )
    action = models.CharField(max_length=50)
    model_name = models.CharField(max_length=100)
    object_id = models.CharField(max_length=50, blank=True)
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Admin audit entry"
        verbose_name_plural = "Admin audit entries"

    def __str__(self):
        return f"{self.action} {self.model_name} ({self.created_at:%Y-%m-%d %H:%M})"
