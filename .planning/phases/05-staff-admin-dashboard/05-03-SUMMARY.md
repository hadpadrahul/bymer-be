# Plan 05-03 Summary — Inquiries, media, home, email, audit

**Status:** Complete

## Delivered

- Contact and career inbox: list (search, status filter), detail (status + internal notes), CSV export
- Email notifications on public form POST via `ADMIN_NOTIFICATION_EMAILS` (`dashboard/services/notifications.py`)
- Media library with `MediaAsset` model, upload view, 10 MB limit
- Dashboard home: counts, health warnings, recent submissions (`dashboard/services/health_checks.py`)
- API reference page and audit log list (last 100 entries)
- Preview link on page detail when `PUBLIC_WEBSITE_BASE_URL` is set

## Notes

- Submissions cannot be deleted from the UI (status workflow only)
- Media library tracks uploads; editors still attach files on individual content forms
