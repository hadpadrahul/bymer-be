# Phase 3: Public API Contract - Context

**Gathered:** 2026-05-23
**Status:** Ready for planning
**Source:** `bymer_project_info.md`, `bymer_be_base_prompt.md`, Phase 2 summaries, `.planning/REQUIREMENTS.md`, `.planning/ROADMAP.md`

<domain>

## Phase Boundary

Phase 3 exposes stable, frontend-friendly public REST APIs on top of the Phase 2 model/admin layer. It should add serializers, filters, pagination, read-only viewsets or API views, URL routing under `/api/`, write-only contact and career form endpoints, page composition for `GET /api/pages/<slug>/`, API tests, and OpenAPI schema coverage.

This phase must not add Docker/Nginx deployment packaging, production handoff sample docs beyond what tests/schema provide, new content models unless a serializer truly cannot be built without a tiny additive field, or public read access to stored form submissions.

</domain>

<decisions>

## Implementation Decisions

### API Structure

- Mount public resources under predictable namespaces:
  - `/api/globals/` for company profile, social links, statistics, and optional global banners.
  - `/api/content/` for repeatable credibility collections.
  - `/api/catalog/` for categories, products, and machinery.
  - `/api/pages/<slug>/` for page-ready composed payloads.
  - `/api/forms/contact/` and `/api/forms/career/` for write-only submissions.
- Keep `core` for health and shared API helpers; add domain `serializers.py`, `views.py`, and `urls.py` per app where practical.
- Include new routes from `config/urls.py` via `include()` — do not bury all views in one monolithic module.

### Read API Behavior

- Public read endpoints use `AllowAny`.
- List endpoints return only `is_active=True` records by default (API-01).
- Preserve model `Meta.ordering` in API ordering; do not invent alternate sort rules unless a requirement needs it.
- Use `django-filter` filter backends already configured in settings for query params defined in `bymer_project_info.md`:
  - `GET /api/content/team/?pillar=true|false`
  - `GET /api/content/testimonials/?type=customer|supplier|other`
  - `GET /api/catalog/products/?category=<slug>`
  - `GET /api/catalog/machinery/?plant=plant_1|plant_2`
- Enable pagination on list endpoints that may grow (team, FAQs, products, machinery, testimonials, timeline, etc.).

### Serializers and Media

- Serializers expose lean, stable field names aligned with frontend needs — no admin-only fields like internal status on public reads.
- Image/file fields return absolute URLs when a request is available; use `SerializerMethodField` or DRF `FileField` with request context.
- Avoid deeply nested serializers except on the page composition endpoint where a bounded payload is intentional.
- Company profile is a singleton retrieved via a dedicated retrieve-style endpoint, not a paginated list.

### Page Composition (PAGE-03, PAGE-04)

- Implement `GET /api/pages/<slug>/` as a dedicated API view, not a generic CMS.
- Resolve `WebsitePage` by slug and `is_active=True`; return 404 for unknown/inactive pages.
- Response includes: `slug`, `title`, optional `meta_title`, optional `meta_description`, `banners`, and a `sections` array.
- Each section item includes a stable `type` string for frontend rendering plus embedded `data` for that section's active ordered records.
- Use a maintainable slug-to-sections mapping module (for example `pages/page_compose.py`) rather than a database-driven page builder.
- Omit optional keys or sections when empty so the frontend can ignore absent content safely.

### Write-Only Forms (FORM-01–03, FORM-06)

- `POST /api/forms/contact/` creates `ContactInquiry` rows with server-side validation.
- `POST /api/forms/career/` creates `JobApplication` rows with server-side validation.
- Do not register inquiry viewsets on the public router — no list, retrieve, update, or delete routes.
- Successful create responses return a minimal acknowledgment payload (for example `{ "success": true }` or `{ "id": ... }`) without exposing admin review fields.
- Accept `source_page` on contact submissions when provided.

### Query Optimization (API-06)

- Use `select_related` for foreign keys (product category, banner page, etc.).
- Use `prefetch_related` where page composition loads multiple collections.
- Keep serializer methods from triggering per-row queries.

### Testing and Schema

- Add API tests with `rest_framework.test.APIClient` for response shapes, active filtering, filters, pagination, validation errors, and form write restrictions.
- Add `@extend_schema` (or equivalent) on new public endpoints so OpenAPI stays accurate.
- Re-run `python manage.py spectacular --validate` after adding endpoints.

### Deferred to Phase 4

- Docker, Nginx, deployment docs, and frontend handoff sample response documents (OPS-02–05).
- Rate limiting, CAPTCHA, and email notifications for forms.
- Resume upload on career applications.

### Agent Discretion

- Exact pagination page size may be chosen conservatively (for example 50) as long as pagination is enabled where required.
- Exact page slug-to-section mapping may start with the known site pages from `bymer_project_info.md` and can be extended when admins add pages — mapping should be easy to edit in code.
- Minor shared helpers in `core/api/` are allowed if they reduce duplication across apps.

</decisions>

<canonical_refs>

## Canonical References

- `bymer_project_info.md` — API endpoint list, hybrid page/collection strategy, filtering rules.
- `bymer_be_base_prompt.md` — lean serializers, stable contracts, performance expectations.
- `.planning/phases/02-admin-content-model-layer/02-01-SUMMARY.md` through `02-03-SUMMARY.md` — implemented models and boundaries.
- `config/settings.py` — DRF and django-filter defaults.
- `config/urls.py`, `core/urls.py` — current API routing pattern.

</canonical_refs>

<deferred>

## Deferred Ideas

- Public caching headers or CDN integration.
- GraphQL or alternate API styles.
- Versioned API (`/api/v2/`).
- Resume file upload on career form.

</deferred>

---

*Phase: 03-public-api-contract*
*Context gathered: 2026-05-23 from source documents and Phase 2 artifacts*
