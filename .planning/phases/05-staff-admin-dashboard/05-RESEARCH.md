# Phase 5: Staff Admin Dashboard - Research

**Date:** 2026-05-25

## Recommended stack (in-repo)

| Piece | Choice | Notes |
|-------|--------|-------|
| Templates | Django templates + `dashboard/templates/` | Extend `base.html` shell |
| CSS | Tailwind via **django-tailwind** or Vite-in-repo static build | Pin version in `requirements.txt` |
| Interactivity | **django-htmx** + Alpine 3 CDN in base | Reorder/toggle partials |
| Forms | ModelForms + `django-crispy-forms` optional | Plain widgets OK if faster |
| Admin API | DRF viewsets under `/api/admin/` | `SessionAuthentication` + `IsAdminUser` |
| Tables | Server-side: `ListView` + `paginate_by` + GET filters | HTMX for filter swap |

## App structure

```
dashboard/
  urls.py          # /dashboard/*
  views/           # split by domain
  forms/
  templates/dashboard/
  templatetags/    # copy_url, warning badges
  registry.py      # content type → list/form urls, public api path
api_admin/         # or dashboard/api/
  urls.py          # /api/admin/*
  views.py
  serializers.py   # staff serializers (include is_active, notes, etc.)
```

## Public API path registry

Maintain `dashboard/lib/public_endpoints.py` mapping model labels to `/api/...` paths so copy buttons stay accurate when routes change.

## Email on submission

Use Django `send_mail` + env `ADMIN_NOTIFICATION_EMAILS` (comma-separated). Trigger in public form create views or signal — keep logic out of templates.

## Audit log (lightweight)

```python
class AdminAuditEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=50)
    model_name = models.CharField(max_length=100)
    object_id = models.CharField(max_length=50)
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
```

Log on create/update/delete/deactivate via mixin or helper — skip read-only list views.

## Settings additions

- `PUBLIC_WEBSITE_BASE_URL`
- `ADMIN_NOTIFICATION_EMAILS`
- `DASHBOARD_MAX_UPLOAD_MB` (default 10)
- Production: `REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES']` without browsable API

## Warnings service

`dashboard/services/health_checks.py` returns queryset of issues for home template context.

## Dependencies to add

- `django-htmx`
- `django-tailwind` (or document `npm run build` for CSS in `dashboard/static/`)

## Risks

- Large phase — split execution into 3–4 plans
- Tailwind build in CI — document in DEVELOPMENT.md
- CSRF + HTMX — use `hx-headers` with CSRF token in base template
