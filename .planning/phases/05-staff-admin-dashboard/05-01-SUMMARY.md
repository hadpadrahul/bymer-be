# Plan 05-01 Summary: Dashboard foundation

## Status

Complete - 2026-05-25

## Delivered

- `dashboard` app: login/logout, staff-only home shell, Tailwind + HTMX + Alpine via CDN
- `/api/admin/health/` with session auth and JSON-only renderer on admin views
- Model fields: `map_url`, `gstin`, banner CTAs, inquiry `internal_notes`
- `AdminAuditEntry` model and migration
- Settings: `PUBLIC_WEBSITE_BASE_URL`, `ADMIN_NOTIFICATION_EMAILS`, `DASHBOARD_MAX_UPLOAD_MB`, login URLs
- `django-htmx` dependency and middleware
- Production: global DRF JSON renderer when `DEBUG=False`
- Tests in `dashboard/tests/test_foundation.py`

## Verification

- `python manage.py migrate` — OK
- `pytest dashboard/` — 5 passed

## Next

Execute `05-02-PLAN.md` — full CRUD modules.
