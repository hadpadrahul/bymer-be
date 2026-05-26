# Roadmap: Bymer Dynamic Website Backend

**Created:** 2026-05-23
**Project Mode:** Vertical MVP
**Granularity:** Coarse

## Overview

This roadmap builds the backend in four vertical phases. Each phase should leave the project more runnable, more testable, and closer to the frontend contract.

**Coverage:** 50 v1 requirements mapped + Phase 5 staff dashboard (extension).

| Phase | Name | Goal | Requirements | Success Criteria |
|-------|------|------|--------------|------------------|
| 1 | Project Foundation | Establish a runnable, testable Django + DRF base with environment configuration and API documentation plumbing. | 6 | 5 |
| 2 | Admin Content Model Layer | Implement the admin-managed data model for global, page, repeatable, catalog, and form content. | 23 | 5 |
| 3 | Public API Contract | Expose stable frontend APIs, write-only form endpoints, filtering, ordering, pagination, and query-conscious serializers. | 17 | 5 |
| 4 | Production Readiness | Package, document, test, and verify the backend for frontend handoff and VPS deployment. | 4 | 5 |
| 5 | Staff Admin Dashboard | Custom `/dashboard/` UI (templates + HTMX) for staff content management; `/api/admin/` for AJAX. | — | 5 |

## Phases

### Phase 1: Project Foundation

**Goal:** Establish a runnable, testable Django + DRF base with environment configuration and API documentation plumbing.
**Mode:** mvp
**UI hint:** no
**Status:** Complete - 2026-05-23

**Requirements:** FOUND-01, FOUND-02, FOUND-03, FOUND-04, FOUND-05, OPS-01

**Success Criteria**:
1. A developer can activate the virtual environment, install dependencies, run migrations, and start the Django server locally.
2. Settings support local SQLite and production PostgreSQL through environment variables without code edits.
3. Static/media settings are explicit and compatible with local development plus production collection/serving.
4. `/api/` routing and OpenAPI/schema endpoints exist, even if later phases add most resources.
5. Pytest is configured and at least a smoke test proves the project boots.

**Primary Work**:
- Create Django project and app structure.
- Add dependency files and environment example.
- Configure DRF, CORS, django-filter, drf-spectacular, static/media, and test settings.
- Add initial health/schema route and smoke tests.

### Phase 2: Admin Content Model Layer

**Goal:** Implement the admin-managed data model for global, page, repeatable, catalog, and form content.
**Mode:** mvp
**UI hint:** no
**Status:** Complete - 2026-05-23

**Requirements:** ADMIN-01, ADMIN-02, ADMIN-03, ADMIN-04, ADMIN-05, GLOB-01, GLOB-02, GLOB-03, GLOB-04, PAGE-01, PAGE-02, CONT-01, CONT-02, CONT-03, CONT-04, CONT-05, CONT-06, CONT-07, CAT-01, CAT-02, CAT-03, FORM-04, FORM-05

**Success Criteria**:
1. Admin can create and manage all required dynamic content models.
2. Repeatable models have ordering and active/published controls.
3. Content-heavy admin screens have useful list displays, search, filters, and field groupings.
4. Catalog models support categories, products, machinery, and plant separation.
5. Contact and career submissions are stored and reviewable in admin.

**Primary Work**:
- Implement global, page, content, catalog, and forms models.
- Add migrations and admin classes.
- Add model validation, ordering defaults, slugs, upload paths, and active flags.
- Add factories or model tests for required fields and common admin-managed states.

### Phase 3: Public API Contract

**Goal:** Expose stable frontend APIs, write-only form endpoints, filtering, ordering, pagination, and query-conscious serializers.
**Mode:** mvp
**UI hint:** no
**Status:** Complete - 2026-05-23

**Requirements:** GLOB-05, PAGE-03, PAGE-04, CONT-08, CAT-04, CAT-05, CAT-06, FORM-01, FORM-02, FORM-03, FORM-06, API-01, API-02, API-03, API-04, API-05, API-06

**Success Criteria**:
1. Frontend can fetch global content, repeatable content, catalog data, and page-ready data through stable endpoints.
2. Products and machinery can be filtered by the required query parameters.
3. Contact and career forms validate input, store submissions, and expose no public list/detail endpoint.
4. Serializers return lean, stable fields with media URLs or metadata suitable for frontend rendering.
5. Common page and collection reads use optimized querysets and avoid serializer-driven query loops.

**Primary Work**:
- Implement serializers, filters, viewsets/API views, pagination, and routers.
- Implement `GET /api/pages/<slug>/` page composition.
- Implement write-only contact and career endpoints.
- Add API tests for response shapes, filters, ordering, validation, and permissions.
- Refine OpenAPI schema annotations.

### Phase 4: Production Readiness

**Goal:** Package, document, test, and verify the backend for frontend handoff and VPS deployment.
**Mode:** mvp
**UI hint:** no

**Requirements:** OPS-02, OPS-03, OPS-04, OPS-05

**Success Criteria**:
1. Docker build and run flow works for the backend service.
2. Production settings for Gunicorn, Nginx, static files, media files, CORS, allowed hosts, and environment variables are documented.
3. Sample API responses or schema usage notes are available for frontend integration.
4. Media backup assumptions for VPS-hosted uploads are documented.
5. Full test suite passes and the roadmap coverage remains 50/50.

**Primary Work**:
- Add Dockerfile, compose/deployment notes, and production environment documentation.
- Add frontend handoff docs with endpoint examples and sample responses.
- Add final test coverage for key models, serializers, endpoints, and deployment assumptions.
- Verify `.gitignore` and branch strategy keep `main` app-clean and `development` GSD-aware.

### Phase 5: Staff Admin Dashboard

**Goal:** Replace day-to-day Django Admin usage with a staff dashboard at `/dashboard/` (Django templates, Tailwind, HTMX) plus `/api/admin/` for AJAX.
**Mode:** mvp
**UI hint:** yes
**Status:** Planned - 2026-05-25

**Depends on:** Phases 2–3 (models + public API). May run in parallel with Phase 4 deploy.

**Success Criteria**:
1. Staff users (`is_staff`) can log in at `/dashboard/` and manage all content types without Django Admin.
2. Globals, pages (known slugs + section map), catalog, content collections, banners, and media are fully CRUD-managed.
3. Contact and career submissions are listable, filterable, exportable (CSV), status/notes editable, not deletable from UI.
4. Dashboard home shows counts, recent submissions, and content health warnings.
5. Edit screens expose copy-public-API-url helpers; API reference page links to `/api/docs/`.

**Primary Work**:
- Model additions (GSTIN, map URL, banner CTAs, inquiry notes, audit log).
- `dashboard` app: views, forms, templates, registry.
- `/api/admin/` endpoints for toggles, reorder, uploads.
- Email on new submissions; lightweight audit log.
- Tests and docs update.

## Requirement Coverage

| Phase | Requirement IDs |
|-------|-----------------|
| 1 | FOUND-01, FOUND-02, FOUND-03, FOUND-04, FOUND-05, OPS-01 |
| 2 | ADMIN-01, ADMIN-02, ADMIN-03, ADMIN-04, ADMIN-05, GLOB-01, GLOB-02, GLOB-03, GLOB-04, PAGE-01, PAGE-02, CONT-01, CONT-02, CONT-03, CONT-04, CONT-05, CONT-06, CONT-07, CAT-01, CAT-02, CAT-03, FORM-04, FORM-05 |
| 3 | GLOB-05, PAGE-03, PAGE-04, CONT-08, CAT-04, CAT-05, CAT-06, FORM-01, FORM-02, FORM-03, FORM-06, API-01, API-02, API-03, API-04, API-05, API-06 |
| 4 | OPS-02, OPS-03, OPS-04, OPS-05 |

## Next Step

Run `$gsd-execute-phase 5` to build the staff admin dashboard (plans 05-01–05-04).

Phase 4 (deploy) can run in parallel: `$gsd-plan-phase 4` if not yet planned.
