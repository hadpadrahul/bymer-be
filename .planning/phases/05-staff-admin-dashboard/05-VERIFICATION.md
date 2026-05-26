# Phase 5 Verification — Staff Admin Dashboard

**Date:** 2026-05-23  
**Result:** Pass

## Automated

| Check | Result |
|-------|--------|
| `pytest` (full suite) | 78 passed |
| Dashboard foundation tests | Pass |
| Dashboard CRUD / API toggle / CSV / email tests | Pass |
| Public `/api/` regression tests | Pass |

## Manual UAT (recommended before production)

- [ ] Staff login/logout at `/dashboard/login/`
- [ ] Non-staff user receives 403 on `/dashboard/`
- [ ] CRUD smoke test per nav section (globals, content, catalog)
- [ ] Page detail shows section links; copy API URL works
- [ ] HTMX toggle active on list row (with CSRF meta)
- [ ] Inquiry status + notes save; CSV export downloads
- [ ] Media upload respects size limit
- [ ] Contact/career POST sends email when `ADMIN_NOTIFICATION_EMAILS` set
- [ ] Mobile sidebar opens/closes (Alpine)

## Security

- Staff-only views (`StaffRequiredMixin` / `@staff_member_required`)
- Session auth + CSRF on dashboard forms and HTMX PATCH to `/api/admin/`
- Public form endpoints unchanged; no delete on submissions

## Documentation

- `docs/ADMIN_DASHBOARD.md` — shipped architecture
- `docs/DEVELOPMENT.md` — staff dashboard section
