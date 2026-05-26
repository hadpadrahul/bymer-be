# Phase 1 Research: Project Foundation

## RESEARCH COMPLETE

## Objective

Research how to implement Phase 1: Project Foundation for a lightweight Django + DRF backend that will later support admin-managed dynamic website content.

## Phase Scope

Phase 1 should create a runnable foundation only:

- Django project scaffold.
- Dependency files.
- Environment-aware settings.
- Static and media configuration.
- DRF `/api/` namespace.
- OpenAPI schema/docs.
- Minimal health endpoint.
- Pytest setup and smoke tests.
- Developer setup documentation.

It should avoid full content models, catalog models, page composition, form submission models, Docker, and production deployment packaging until later phases.

## Recommended Technical Approach

### Project Layout

Use a conventional Django layout:

- `manage.py`
- `config/` for project settings, URL routing, ASGI, and WSGI.
- `core/` for the minimal health endpoint and future shared primitives.
- `core/tests/` for Phase 1 smoke tests.
- `.env.example` for required configuration.
- `requirements.txt` for runtime dependencies.
- `requirements-dev.txt` for test/development dependencies.
- `pytest.ini` for pytest-django settings.
- `README.md` for local setup and validation commands.

This keeps Phase 1 small while giving later phases a stable place to add app modules.

### Settings Pattern

Use a single environment-aware `config/settings.py` for Phase 1. Separate settings modules can be introduced later only if production complexity justifies them.

Required environment keys:

- `DJANGO_SECRET_KEY`
- `DJANGO_DEBUG`
- `DJANGO_ALLOWED_HOSTS`
- `DATABASE_URL`
- `DJANGO_CORS_ALLOWED_ORIGINS`

Defaults can support local development:

- SQLite database at `BASE_DIR / "db.sqlite3"` when `DATABASE_URL` is absent.
- `DEBUG=True` locally.
- `ALLOWED_HOSTS=localhost,127.0.0.1`.

### Dependency Set

Runtime:

- `Django`
- `djangorestframework`
- `django-environ`
- `django-cors-headers`
- `django-filter`
- `drf-spectacular`
- `Pillow`
- `gunicorn`
- `whitenoise`
- `psycopg2-binary`

Development/test:

- `pytest`
- `pytest-django`
- `factory_boy`
- `Faker`

Pinning exact versions can happen during implementation by installing current compatible releases into the active environment and freezing or writing explicit constraints.

### API Skeleton

Provide these Phase 1 URLs:

- `/admin/`
- `/api/health/`
- `/api/schema/`
- `/api/docs/`

The health endpoint should return a small stable JSON payload, such as `{"status": "ok"}`. It should not require database content or authentication.

### Testing

Minimum tests:

- Django URL configuration imports and the app can boot under pytest.
- `GET /api/health/` returns HTTP 200 and `{"status": "ok"}`.
- `GET /api/schema/` returns HTTP 200.
- Static/media settings exist and point at configured locations.

Use pytest-django with `DJANGO_SETTINGS_MODULE=config.settings`.

### Walking Skeleton Interpretation

Because this is a backend-only project, the walking skeleton proves the backend stack rather than a browser UI:

- Project scaffold exists.
- A real route is served under `/api/`.
- Django can run migrations against SQLite locally, proving database connectivity and writes to the migration table.
- OpenAPI schema generation proves DRF integration.
- Tests prove boot, routing, and schema availability.
- README commands prove the local development flow.

## Risks and Mitigations

| Risk | Mitigation |
|------|------------|
| Phase 1 grows into content modeling | Keep models for globals/pages/catalog/forms deferred to Phase 2. |
| Settings become too clever | Use one clear env-aware settings module for now. |
| Dependency drift | Install latest compatible packages during execution, then record exact working dependencies. |
| Schema endpoint fails without API views | Include a simple health API view and drf-spectacular configuration. |
| Production assumptions remain vague | Add env, static, media, and PostgreSQL configuration now; defer Docker/Nginx details to Phase 4. |

## Validation Architecture

Phase 1 can be validated with deterministic local commands:

- `python manage.py check`
- `python manage.py migrate`
- `pytest`
- Optional manual run: `python manage.py runserver`

These commands should pass before Phase 1 is marked complete.

## Plan Implications

Create one sequential plan for Phase 1 because the scaffold, settings, URLs, and tests all touch shared files and should not run in parallel. The plan should include a formal `<threat_model>` block because settings, CORS, secrets, and public API routes are security-relevant even in foundation work.
