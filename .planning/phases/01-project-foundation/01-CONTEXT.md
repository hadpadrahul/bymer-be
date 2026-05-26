# Phase 1: Project Foundation - Context

**Gathered:** 2026-05-23
**Status:** Ready for planning
**Source:** User-provided project source documents and initialized GSD project artifacts

<domain>

## Phase Boundary

Phase 1 establishes the smallest runnable Django + DRF backend foundation for the Bymer dynamic website project. It should create the project scaffold, dependency management, environment-aware settings, `/api/` routing, schema documentation plumbing, static/media configuration, and a smoke-tested local development path.

This phase must not implement the full content model, catalog model, forms, or page assembly API. Those belong to later phases. It may create only minimal placeholder routes or health/schema endpoints needed to prove the backend boots and the API namespace exists.

</domain>

<decisions>

## Implementation Decisions

### Locked Stack

- Use Django + Django REST Framework as the backend framework.
- Use Django Admin as the internal content-management interface; do not build a custom admin UI.
- Use SQLite for local development and PostgreSQL for production through `.env` configuration.
- Use `django-environ` for environment-based settings.
- Use `django-cors-headers` for frontend integration readiness.
- Use `django-filter` for future list filtering support.
- Use `drf-spectacular` for OpenAPI/schema documentation.
- Use `Pillow` for image upload support.
- Use `gunicorn` and `whitenoise` as production-ready baseline dependencies.
- Use `pytest`, `pytest-django`, `factory_boy`, and `Faker` for test infrastructure.

### Project Shape

- Keep the backend small, admin-friendly, and production-friendly.
- Prefer explicit Django apps over a generic CMS/page-builder abstraction.
- Planned app boundaries are `core`, `pages`, `globals`, `content`, `catalog`, `forms`, and optionally `api`; Phase 1 should create only the foundational structure needed now.
- Use stable `/api/` routing from the start.
- Include OpenAPI/schema endpoints in Phase 1 even before most resources exist.

### Environment and Deployment Foundation

- Use `.env` values for secret key, debug mode, allowed hosts, database URL, CORS origins, static/media settings where appropriate, and any production-sensitive configuration.
- Keep `.env` untracked and provide `.env.example`.
- Local development may use SQLite without requiring PostgreSQL.
- Production configuration must be ready to point at PostgreSQL without code changes.
- Media is expected to live under `media/` on the VPS and be served by Nginx later.
- Static assets must support collection/serving for production.

### Branch and Repository Policy

- Work happens on `development`.
- `main` should remain app-clean and not carry GSD planning artifacts.
- `.planning/` is intentionally tracked on `development`.
- Agent/runtime directories such as `.codex/`, `.cursor/`, `.gemini/`, `.claude/`, `.agent/`, `.agents/`, and local virtual environments must stay untracked.

### Phase 1 Requirements

- `FOUND-01`: Developer can install and run a Django + DRF project locally using documented environment variables.
- `FOUND-02`: Developer can use SQLite locally and configure PostgreSQL for production through `.env` settings.
- `FOUND-03`: Developer can manage static and uploaded media through configured `STATIC_*` and `MEDIA_*` settings.
- `FOUND-04`: API consumer can access all public API endpoints under a consistent `/api/` URL namespace.
- `FOUND-05`: Developer can view generated OpenAPI documentation for the public API.
- `OPS-01`: Developer can run automated tests for models, serializers, and API endpoints.

### the agent's Discretion

- Exact Python package version pins may be selected during implementation, but should prefer current stable compatible releases.
- Exact Django project package name may be chosen for clarity, as long as it is consistent and not overly clever.
- Whether to use a central `api` app in Phase 1 is discretionary if routing remains clean.
- Exact health endpoint shape is discretionary, but it must be simple and useful for smoke testing.
- The executor may decide whether to include a minimal base model now or defer it to Phase 2 if it would add unnecessary surface area.

</decisions>

<canonical_refs>

## Canonical References

Downstream agents MUST read these before planning or implementing.

### Project Source

- `bymer_project_info.md` - primary source of truth for project scope, content strategy, API shape, admin requirements, performance expectations, and deployment assumptions.
- `bymer_be_base_prompt.md` - implementation guidance and engineering guardrails for the backend.
- `.planning/PROJECT.md` - living project context and constraints.
- `.planning/REQUIREMENTS.md` - v1 requirements and Phase 1 requirement mapping.
- `.planning/ROADMAP.md` - phase goals, success criteria, and MVP mode.
- `.planning/research/STACK.md` - recommended stack and dependency boundaries.
- `.planning/research/ARCHITECTURE.md` - intended app boundaries and data-flow direction.
- `.planning/research/SUMMARY.md` - summarized research findings and roadmap shape.

</canonical_refs>

<specifics>

## Specific Ideas

- Create a Django project that can run with `python manage.py runserver`.
- Provide dependency files suitable for installing Django, DRF, environment/config, schema, CORS, filtering, image, production server, and test packages.
- Add `.env.example` with the required environment variables.
- Configure `MEDIA_URL`, `MEDIA_ROOT`, `STATIC_URL`, `STATIC_ROOT`, and Whitenoise/static behavior.
- Add DRF and drf-spectacular URLs under `/api/`, including schema and documentation routes.
- Add a minimal health endpoint or smoke route under `/api/` so tests can prove routing works.
- Configure pytest so `pytest` can run without special manual setup.
- Add smoke tests for project boot, API namespace availability, and schema endpoint availability.
- Add a short README or development note explaining setup, env vars, runserver, migrations, tests, and API docs.

</specifics>

<deferred>

## Deferred Ideas

- Full dynamic content models are deferred to Phase 2.
- Catalog, machinery, form submission models, and admin classes are deferred to Phase 2.
- Public collection APIs, page composition, filtering behavior, and write-only form endpoints are deferred to Phase 3.
- Docker, Nginx deployment packaging, production docs, and sample frontend handoff responses are deferred to Phase 4 except for foundational settings that make them possible.
- Email notifications, resume uploads, caching, object storage, and anti-spam tooling remain v2/future scope.

</deferred>

---

*Phase: 01-project-foundation*
*Context gathered: 2026-05-23 from source documents and GSD project artifacts*
