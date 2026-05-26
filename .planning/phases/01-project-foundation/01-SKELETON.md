# Walking Skeleton - Bymer Dynamic Website Backend

**Phase:** 1
**Generated:** 2026-05-23

## Capability Proven End-to-End

A developer can run the Django backend locally, hit `/api/health/`, inspect `/api/schema/` or `/api/docs/`, and run tests that prove the project boots with configured settings.

## Architectural Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Framework | Django + Django REST Framework | Fits admin-first content management and stable REST APIs. |
| Data layer | SQLite locally, PostgreSQL via `DATABASE_URL` in production | Keeps local setup light while preserving production readiness. |
| Auth | Django admin/staff authentication only for now | Public user accounts are out of scope. |
| Configuration | `django-environ` with `.env.example` | Makes local and production settings explicit without code changes. |
| API docs | `drf-spectacular` at `/api/schema/` and `/api/docs/` | Gives the frontend a discoverable contract from the start. |
| Directory layout | `config/` project package plus `core/` foundation app | Keeps the scaffold conventional and leaves domain apps for later phases. |
| Static/media | Whitenoise for static baseline, `media/` for local uploads | Matches the later VPS + Nginx static/media serving plan. |

## Stack Touched in Phase 1

- [ ] Project scaffold: Django project, dependency files, test runner.
- [ ] Routing: `/api/health/`, `/api/schema/`, `/api/docs/`, and `/admin/`.
- [ ] Database: local migrations can write/read the SQLite migration state.
- [ ] API interaction: health endpoint returns a real JSON response.
- [ ] Development run path: documented local commands for install, migrate, runserver, and tests.

## Out of Scope (Deferred to Later Slices)

- Global/page/content/catalog/form models.
- Admin classes for dynamic website content.
- Public collection APIs and page composition.
- Contact/career write endpoints.
- Docker and Nginx deployment packaging.
- Email notifications, resume uploads, object storage, anti-spam, and caching.

## Subsequent Slice Plan

Each later phase adds one vertical backend slice on top of this skeleton without changing its foundation decisions:

- Phase 2: Admin-managed content model layer.
- Phase 3: Public API contract and write-only form endpoints.
- Phase 4: Production readiness, frontend handoff docs, Docker, and deployment verification.
