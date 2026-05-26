# Phase 3 Research: Public API Contract

## RESEARCH COMPLETE

## Objective

Research how to implement Phase 3 public REST APIs on the existing Phase 2 Django apps without overbuilding a CMS or leaking form submissions.

## Existing Foundation

Phase 2 provides:

- Apps: `site_settings`, `pages`, `content`, `catalog`, `inquiries` with migrations and admin.
- DRF installed with `django-filter` as default filter backend.
- `drf-spectacular` for OpenAPI at `/api/schema/` and `/api/docs/`.
- Health check at `/api/health/` via `core.urls`.
- pytest-django and APIClient used in Phase 1 smoke tests.

Phase 3 should extend each domain app with serializers/views/urls rather than introducing a new API framework layer.

## Recommended Technical Approach

### Shared API Conventions

Create small shared helpers under `core/api/` (or `core/api.py`):

- `ActiveQuerysetMixin` — `get_queryset()` filters `is_active=True`.
- `AbsoluteMediaUrlMixin` or utility `build_media_url(request, file_field)` for consistent media URLs (API-05).
- Optional `StandardPagination` class registered in `REST_FRAMEWORK` or per-viewset.

Update `REST_FRAMEWORK` in `config/settings.py`:

```python
"DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.AllowAny"],
"DEFAULT_PAGINATION_CLASS": "core.api.pagination.StandardPagination",
"PAGE_SIZE": 50,
```

Public form views can override permissions if stricter rules are added later; reads stay `AllowAny`.

### Globals (`site_settings`)

| Endpoint | View pattern | Notes |
|----------|--------------|-------|
| `GET /api/globals/company-profile/` | `RetrieveAPIView` | Return the singleton row; 404 if missing |
| `GET /api/globals/social-links/` | `ReadOnlyModelViewSet` | Ordered active links |
| `GET /api/globals/statistics/` | `ReadOnlyModelViewSet` | Ordered active stats |
| `GET /api/globals/banners/` | `ReadOnlyModelViewSet` | Optional; filter by `page` slug query param if useful |

Serializers should expose frontend fields only (name, urls, labels, values, banner media URLs).

### Content Collections (`content`)

Use `ReadOnlyModelViewSet` per model with shared list/retrieve patterns:

- `team`, `timelines`, `clients`, `testimonials`, `certifications`, `awards`, `faqs`

Filters:

- `TeamMemberFilter`: `pillar` boolean query maps to `is_management_pillar`.
- `TestimonialDocumentFilter`: `type` choice filter.

All lists: active-only, paginated, ordered.

### Catalog (`catalog`)

| Endpoint | Filters |
|----------|---------|
| `GET /api/catalog/categories/` | active only |
| `GET /api/catalog/products/` | `category` slug via FK |
| `GET /api/catalog/machinery/` | `plant` exact match |

Use `select_related("category")` on products. Slug filters should 404 or return empty queryset — prefer empty list for unknown category slug to keep frontend simple.

### Page Composition (`pages`)

`PageDetailView` (APIView or generic retrieve by slug):

1. Load `WebsitePage` by slug + active.
2. Load page-linked `SiteMediaBanner` queryset (active, ordered).
3. Build `sections` from `PAGE_SECTION_MAP[slug]` — each entry defines `type` and a callable or queryset key to serialize.
4. Return combined JSON; omit empty optional fields.

Example mapping (illustrative):

| Slug | Sections |
|------|----------|
| `home` | banners, statistics |
| `our-team` | team |
| `our-history` | timelines |
| `testimonials` | testimonials |
| `quality-assurance` | certifications, awards |
| `automotive-products` | products (category slug TBD in admin) |
| `machinery` | machinery grouped or flat list |

Executors may align category slugs with real admin data; mapping must be documented in code comments.

### Write-Only Forms (`inquiries`)

| Endpoint | View | Methods |
|----------|------|---------|
| `/api/forms/contact/` | `CreateAPIView` | POST only |
| `/api/forms/career/` | `CreateAPIView` | POST only |

Serializers:

- `ContactInquiryCreateSerializer` — writable fields only; set `status=new` in `create()`.
- `JobApplicationCreateSerializer` — match model fields; validate required fields per FORM-02/03.

Explicitly do **not** add router routes for inquiries. Verify with tests that GET returns 405/404.

### URL Wiring

`config/urls.py`:

```python
path("api/globals/", include("site_settings.urls")),
path("api/content/", include("content.urls")),
path("api/catalog/", include("catalog.urls")),
path("api/pages/", include("pages.urls")),
path("api/forms/", include("inquiries.urls")),
path("api/", include("core.urls")),
```

Order matters: more specific prefixes before the catch-all `core` include if paths could collide.

### Testing Strategy

Per app `tests/test_api.py`:

- Status 200 on list/retrieve for active records.
- Inactive records excluded from lists.
- Filter query params return expected subsets.
- Page endpoint 404 for bad slug.
- Page response includes expected section `type` keys when data exists.
- Form POST success creates DB row.
- Form GET not allowed.
- Invalid payload returns 400 with field errors (FORM-03).

Use factories or direct `objects.create()` consistent with Phase 2 tests.

### OpenAPI

Add `@extend_schema` on class-based views and viewsets. Re-run:

`python manage.py spectacular --file schema.yml --validate`

## Risks and Mitigations

| Risk | Mitigation |
|------|------------|
| Page composition becomes a page builder | Static slug map + embedded serializers only |
| N+1 queries on page endpoint | Prefetch section querysets; limit section count |
| Form spam / abuse | Document deferral to v2; validate required fields now |
| Inquiry data leaked via API | No read routes; tests assert GET forbidden |
| Serializer scope creep | One serializer per public resource; separate create serializers for forms |
| OpenAPI drift | Schema annotations on all new views |

## Plan Implications

Use four sequential plans:

1. **03-01** — Shared API helpers, settings, globals endpoints, tests.
2. **03-02** — Content collection read APIs with filters and pagination.
3. **03-03** — Catalog read APIs with filters; page composition endpoint.
4. **03-04** — Write-only forms, cross-domain API verification, OpenAPI validation.

Sequential waves avoid URL/router merge conflicts and let later plans import serializer patterns from earlier apps.
