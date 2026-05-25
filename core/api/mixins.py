class ActiveQuerysetMixin:
    """Limit public list/retrieve querysets to active records."""

    def get_queryset(self):
        queryset = super().get_queryset()
        if hasattr(queryset.model, "is_active"):
            return queryset.filter(is_active=True)
        return queryset
