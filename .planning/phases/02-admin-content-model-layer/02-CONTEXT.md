# Phase 2: Admin Content Model Layer - Context

**Gathered:** 2026-05-23
**Status:** Ready for planning
**Source:** User-provided project source documents, Phase 1 summary, and GSD roadmap/requirements

<domain>

## Phase Boundary

Phase 2 implements the admin-managed data model layer for the Bymer dynamic website backend. It should add Django apps, models, migrations, admin classes, model/admin-focused tests, and any small shared model helpers needed to manage global content, page metadata, repeatable credibility content, catalog content, and stored form submissions.

This phase must not build public API serializers, viewsets, routers, page-composition endpoints, filtering endpoints, Docker deployment, Nginx configuration, or frontend handoff examples. Those belong to Phases 3 and 4. It may prepare model fields and relationships that make the later API contract straightforward.

</domain>

<decisions>

## Implementation Decisions

### App Boundaries

- Create explicit Django apps for the content domains rather than one generic CMS app.
- Use these package names unless implementation discovers a blocking Django conflict:
  - `site_settings` for global/company/site-wide models.
  - `pages` for known page records and page-to-banner/helper relationships.
  - `content` for repeatable credibility/content collections.
  - `catalog` for product and machinery data.
  - `inquiries` for contact and career submission storage.
- Avoid app package names such as `forms` that can be confused with `django.forms`.
- Add all Phase 2 apps to `INSTALLED_APPS`.

### Shared Model Patterns

- Prefer normalized relational models.
- Use explicit `order` integer fields for repeatable content.
- Use `is_active` booleans for hide/show behavior.
- Use `slug` fields where the frontend or admin needs stable identifiers.
- Use `created_at` and `updated_at` timestamps where records are operational or likely audited.
- Use `ImageField` or `FileField` only on models that actually need media assets.
- Keep upload paths grouped by domain, such as `banners/`, `team/`, `products/`, `machinery/`, and `documents/`.
- Keep JSONField out of the initial model layer unless the specific model truly needs flexible structured data.

### Global and Page Models

- Implement a singleton-style `CompanyProfile` for brand and contact details.
- Implement `SocialLink`, `CompanyStatistic`, and `SiteMediaBanner`.
- Implement a known-page model that can represent the current website pages by slug, title, optional metadata, active status, and ordering.
- Allow page-specific helper relationships where needed, but do not implement a full page builder or arbitrary section composition in Phase 2.

### Repeatable Content Models

- Implement repeatable admin-managed models for team members, timeline/history items, clients/partners, testimonials/documents, certifications, awards, and FAQs.
- Include fields from `bymer_project_info.md` where listed, plus minimal practical fields for admin usability.
- Include search, filters, ordering, and list displays in admin where useful.

### Catalog Models

- Implement `ProductCategory`, `Product`, and `Machinery`.
- Use either a `MachineryPlant` model or a constrained plant field. Prefer the simpler option unless the implementation needs plant records as independent admin-managed objects.
- Products and machinery must have deterministic ordering and active flags.
- Products must support category relationships and future filtering by category slug.
- Machinery must support future filtering by plant.

### Form Submission Models

- Implement `ContactInquiry` and `JobApplication` as stored submission models visible in admin.
- Do not implement public write endpoints in this phase.
- Career submissions should be ready for a future `resume_file` field if later approved, but do not add resume upload unless needed now.
- Admin should make submissions reviewable/searchable/filterable.

### Testing Scope

- Add model tests for required fields, string representations, ordering defaults, singleton behavior, slugs, and core validation.
- Add admin registration smoke tests or admin configuration tests where practical.
- Use pytest/pytest-django and factory_boy/Faker consistent with Phase 1.

### Deferred to Later Phases

- Public API serializers, viewsets, filtering, pagination, and page composition are Phase 3.
- Production Docker/Nginx packaging and deployment docs are Phase 4.
- Email notifications, CAPTCHA, object storage, reusable document libraries, richer SEO, caching, and career resume upload remain v2/future unless later confirmed.

### the agent's Discretion

- Exact field lengths and optional/blank settings may be selected conservatively based on Django conventions and project needs.
- Exact admin fieldsets and preview helpers may be chosen for practical editor usability.
- Model verbose names may be adjusted to make Django Admin non-technical friendly.
- If a planned model would add more complexity than value, the executor may simplify it only when the relevant requirement still remains satisfied and the reason is documented.

</decisions>

<canonical_refs>

## Canonical References

Downstream agents MUST read these before planning or implementing.

### Project Source

- `bymer_project_info.md` - primary source of truth for content strategy, model list, admin needs, site pages, dynamic/static split, and API direction.
- `bymer_be_base_prompt.md` - implementation guardrails for simple, admin-friendly, fast Django/DRF backend work.
- `.planning/PROJECT.md` - living project constraints and decisions.
- `.planning/REQUIREMENTS.md` - Phase 2 requirement IDs and traceability.
- `.planning/ROADMAP.md` - Phase 2 goal, success criteria, mode, and primary work.
- `.planning/phases/01-project-foundation/01-01-SUMMARY.md` - established Phase 1 project/app/settings/test patterns.

### Existing Code

- `config/settings.py` - current installed apps and settings pattern.
- `core/apps.py` - app config style established in Phase 1.
- `pytest.ini` - pytest-django configuration.
- `requirements-dev.txt` - available test libraries.

</canonical_refs>

<specifics>

## Specific Ideas

- Create model/admin work in small domain slices to keep migrations and tests reviewable.
- Keep public-facing endpoint paths in mind, but do not create endpoints yet.
- Prefer `is_active` over mixed `active`/`published` naming unless a model has a clear separate publishing lifecycle.
- Use admin list filters for `is_active`, category/type fields, plant, created dates, and content type fields.
- Use `prepopulated_fields` for slugs where practical.
- Add helpful `__str__` methods for all admin-managed models.
- Create migrations in the same phase as the models.

</specifics>

<deferred>

## Deferred Ideas

- `GET /api/pages/<slug>/` and collection endpoints are deferred to Phase 3.
- Serializer field selection, query optimization for API reads, filtering, pagination, and write-only form endpoints are deferred to Phase 3.
- Docker, Nginx, production settings docs, and frontend sample responses are deferred to Phase 4.
- Resume upload support is deferred until the client explicitly approves it.

</deferred>

---

*Phase: 02-admin-content-model-layer*
*Context gathered: 2026-05-23 from source documents and Phase 1 artifacts*
