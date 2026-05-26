# Phase 2 Pattern Map

## Existing Patterns to Reuse

| New area | Closest existing analog | Pattern to follow |
|----------|-------------------------|-------------------|
| Django app packages | `core/apps.py` | Use a simple `AppConfig` with `default_auto_field = "django.db.models.BigAutoField"` and `name = "<app_package>"`. |
| Settings registration | `config/settings.py` | Add new domain apps to `INSTALLED_APPS` as plain app package strings near `core`. |
| Tests | `core/tests/test_foundation.py` | Use pytest functions, clear assertions, and Django/DRF test helpers only when needed. |
| Environment/settings style | `config/settings.py` | Keep settings explicit and simple; avoid extra settings modules until production complexity requires them. |
| URL/API boundary | `config/urls.py` and `core/urls.py` | Do not add Phase 2 public URLs; keep API routing changes for Phase 3. |

## Phase 2 File Families

### Domain Apps

New apps should be ordinary Django apps:

- `site_settings`
- `pages`
- `content`
- `catalog`
- `inquiries`

Each app should have:

- `__init__.py`
- `apps.py`
- `models.py`
- `admin.py`
- `migrations/__init__.py`
- app-local tests under `tests/`

### Model Conventions

Use repeated field conventions where applicable:

- `order`
- `is_active`
- `created_at`
- `updated_at`
- `slug`

Admin classes should expose these fields consistently through list displays, filters, search fields, and ordering.

## Non-Patterns

- Do not create serializers, viewsets, routers, or API endpoints in Phase 2.
- Do not introduce a generic page-builder or CMS abstraction.
- Do not add third-party dependencies for singleton models, image previews, or admin enhancements unless a later phase proves the need.
