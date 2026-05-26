from dashboard.models import AdminAuditEntry


def log_audit(request, *, action: str, model_name: str, object_id="", message: str = ""):
    if not request.user.is_authenticated:
        return
    AdminAuditEntry.objects.create(
        user=request.user,
        action=action,
        model_name=model_name,
        object_id=str(object_id) if object_id else "",
        message=message[:500],
    )
