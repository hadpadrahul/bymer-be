# Phase 5: Staff Admin Dashboard - Context

**Gathered:** 2026-05-25
**Status:** Ready for planning
**Source:** User decisions (2026-05-25), `docs/ADMIN_DASHBOARD.md`, Phase 2–3 artifacts, live models/APIs

<domain>

## Phase Boundary

Deliver a **production admin UI** at `/dashboard/` using **Django templates**, **ModelForms**, **Tailwind CSS**, **HTMX**, and **minimal Alpine.js**. Supplement with **`/api/admin/`** JSON endpoints only where AJAX helps (reorder, toggles, uploads, copy helpers, table filters).

Editors use this instead of Django Admin for day-to-day work. **Django Admin remains** as superuser/developer fallback.

Public `/api/*` read/write contract from Phase 3 **must not break**.

This phase is **not** a generic CMS, not a separate SPA repo, and not a DB-driven page builder. Page sections stay **code-mapped** via `pages/page_compose.py`.

Phase 4 (Docker/deploy) may proceed in parallel; dashboard completion does not block minimal production API deploy.

</domain>

<decisions>

## Implementation Decisions

### Access and URLs

- **D-01:** URL prefix `/dashboard/` on same app host (e.g. `api.domain.com/dashboard/`).
- **D-02:** `login_required` + `is_staff` on all dashboard views; CSRF on all mutations.
- **D-03:** Login/logout only for v1; password reset/change deferred.
- **D-04:** Post-login landing = dashboard home.
- **D-05:** Single editor role for v1 (`is_staff`); no per-model permissions yet.
- **D-06:** Django Admin stays available; dashboard is primary for editors.

### UI stack

- **D-07:** Tailwind CSS for styling; neutral clean admin theme.
- **D-08:** HTMX + minimal Alpine.js; no React/Vite/external frontend.
- **D-09:** Server-side pagination, search, filter on list views.
- **D-10:** Django messages + lightweight JS toasts where helpful.
- **D-11:** Responsive: collapsible sidebar desktop; stacked mobile; desktop-primary workflow.

### CRUD pattern

- **D-12:** Default = Django class-based views + ModelForms + templates per resource.
- **D-13:** AJAX via `/api/admin/` for: `order` updates, `is_active` toggles, image upload/preview helpers, copy-endpoint actions, enhanced table filter/search.
- **D-14:** Disable DRF browsable API in production for admin routes.
- **D-15:** Prefer `is_active=False` over hard delete; hard delete only with confirm for safe cases.
- **D-16:** Block category delete when products reference it.
- **D-17:** Ordering via numeric `order` field; optional drag/drop later if low cost.

### Content scope (full modules)

- **D-18:** Build complete UI for all existing managed entities: company profile, social links, statistics, banners, pages (known slugs), all content collections, catalog, inquiries (contact + career), media library, API reference page, dashboard home with warnings.
- **D-19:** Pages: editors manage **existing slugs only**; detail view shows **read-only section map** from `page_compose` + links to underlying collections.
- **D-20:** Do not build DB-driven section builder or generic content engine.

### Model additions (smallest practical)

- **D-21:** `CompanyProfile`: add `map_url`, `gstin` (blank allowed).
- **D-22:** `SiteMediaBanner`: add `cta_text`, `cta_button_url` (blank allowed).
- **D-23:** `ContactInquiry` / `JobApplication`: add `internal_notes` (blank).
- **D-24:** Email notification on new contact/career submission (in scope).
- **D-25:** Lightweight audit log if simple (model: user, action, model, object_id, timestamp, optional message).
- **D-26:** `PUBLIC_WEBSITE_BASE_URL` env for “preview public page” links.

### Submissions

- **D-27:** List columns: name, email, phone, date, status.
- **D-28:** Status: `new` | `reviewed` | `closed`; editable + internal notes.
- **D-29:** No delete in UI for inquiries/applications.
- **D-30:** CSV export for both types.

### Media

- **D-31:** Standalone media library page + uploads on entity forms.
- **D-32:** Images + PDFs/documents where models support files; validation + size limits.
- **D-33:** “Where used” deferred.

### API helper (frontend dev UX)

- **D-34:** Every edit/detail screen: copy public API URL + copy resource path.
- **D-35:** Central `/dashboard/api-reference/` linking to `/api/docs/`; copy-only (no live JSON preview).

### Dashboard home

- **D-36:** Prioritize: recent submissions, total counts, missing-image warnings, inactive-content warnings.
- **D-37:** Warnings include: missing image, inactive record, empty category, product without image, inactive page with active banner.

### Architecture / extensibility

- **D-38:** New Django app `dashboard` (templates, views, forms, urls); admin API under `core` or `dashboard/api/`.
- **D-39:** Registry pattern for content types so future modules (e.g. “Compounds”) add list/form URLs without rewriting shell.
- **D-40:** Avoid i18n assumptions in labels; keep field-driven forms.

### Testing

- **D-41:** Django client tests for views/forms; API tests for `/api/admin/` AJAX endpoints.

### Agent discretion

- Exact Tailwind build pipeline (django-tailwind vs compiled static).
- Audit log granularity if too heavy for v1 — ship minimal version or defer with flag.
- HTMX partial template naming conventions.

</decisions>

<specifics>

## Specific Ideas

- Non-technical editors: clear labels, grouped forms, confirmation on destructive actions.
- Frontend developers: visible public endpoint paths on every resource screen.
- Upload UX: thumbnail preview, replace image in place.
- Warnings on home should be actionable (link to fix).

</specifics>

<canonical_refs>

## Canonical References

### Product and API
- `bymer_project_info.md` — site structure, filters, content types
- `docs/API.md` — public endpoint contract
- `pages/page_compose.py` — slug → section mapping (read-only in UI)

### Prior phases
- `.planning/phases/02-admin-content-model-layer/02-CONTEXT.md` — models/admin baseline
- `.planning/phases/03-public-api-contract/03-CONTEXT.md` — public API rules

</canonical_refs>

<code_context>

## Existing Code Insights

### Reusable Assets
- All Phase 2 models + Django Admin field groupings as UX reference
- `core/api/fields.py` — `build_absolute_media_url` for copy helpers
- `ActiveQuerysetMixin`, `StandardPagination` patterns from public API
- Public serializers as reference for field names on copy-helper text

### Integration Points
- `config/urls.py` — include `dashboard.urls` at `dashboard/`
- `INSTALLED_APPS` — add `dashboard`, `django_htmx` (if used)
- `REST_FRAMEWORK` — separate permission defaults for `/api/admin/`
- Phase 3 public routes unchanged

### Gaps to build
- No `/api/admin/` today
- No `/dashboard/` views
- Missing model fields per D-21–D-23
- No email on form submit
- Banners lack CTA fields in DB today

</code_context>

<deferred>

## Deferred Ideas

- DB-driven page section builder
- Password reset/change in dashboard
- Per-model permission groups
- Media “where used” graph
- Live JSON preview on API helper
- Drag-and-drop ordering (unless trivial with HTMX)
- Full i18n
- Browsable DRF admin in dev only (optional later)

</deferred>

---

*Phase: 05-staff-admin-dashboard*
*Context gathered: 2026-05-25*
