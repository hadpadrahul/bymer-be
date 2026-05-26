# Phase 3 Pattern Map

## Existing Patterns to Reuse

| New area | Closest existing analog | Pattern to follow |
|----------|-------------------------|-------------------|
| API smoke tests | `core/tests/test_foundation.py` | Use `APIClient`, assert status codes and response keys |
| Health/schema views | `core/views.py` | Use `@extend_schema` for OpenAPI on function views |
| App packaging | Phase 2 apps | Add `serializers.py`, `views.py`, `urls.py`, `tests/test_api.py` per domain app |
| Settings | `config/settings.py` | Extend `REST_FRAMEWORK` dict; keep env-based config |
| URL mounting | `config/urls.py` | `path("api/...", include("app.urls"))` |

## Phase 3 File Families

### Shared API (`core/api/`)

- `pagination.py` — standard page size for list endpoints
- `mixins.py` — active-only queryset, media URL helper
- Optional `permissions.py` if defaults differ per area

### Per-App API Modules

Each content app gains:

- `serializers.py` — public read serializers (+ create serializers in `inquiries`)
- `views.py` — viewsets or API views
- `urls.py` — router or explicit paths
- `filters.py` — django-filter `FilterSet` where query params are required
- `tests/test_api.py` — endpoint behavior tests

### Page Composition

- `pages/page_compose.py` — slug → sections mapping and assembly logic
- `pages/views.py` — `PageDetailView`
- `pages/serializers.py` — page and section payload serializers

## API Conventions

- Read: `ReadOnlyModelViewSet` or `RetrieveAPIView` with `AllowAny`.
- Write forms: `CreateAPIView` only; no router registration for inquiries list/detail.
- Querysets: filter `is_active=True`; `select_related` / `prefetch_related` on FK paths.
- Responses: stable keys, ordered arrays, optional fields omitted when empty on page endpoint.
- Media: absolute URLs in API output.

## Non-Patterns

- Do not add django-guardian or public user accounts.
- Do not expose `ContactInquiry` or `JobApplication` on GET.
- Do not add a `PageSection` database model in Phase 3.
- Do not create one endpoint per marketing paragraph variant — use filters on stable collections.
