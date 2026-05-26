# Phase 2 Research: Admin Content Model Layer

## RESEARCH COMPLETE

## Objective

Research how to implement Phase 2: Admin Content Model Layer for the Bymer dynamic website backend. The plan must establish admin-managed Django models, migrations, admin classes, and model/admin tests without building public API endpoints yet.

## Phase Scope

Phase 2 should add:

- Domain-specific Django apps for global/site settings, pages, repeatable content, catalog data, and stored inquiries.
- Models and migrations for all Phase 2 requirements.
- Django Admin registrations with practical list displays, search, filters, ordering, fieldsets, and useful media/file identification.
- Tests for model behavior and core admin registration/configuration.

Phase 2 should avoid:

- DRF serializers, viewsets, routers, and frontend API response shaping.
- Page composition endpoints.
- Docker/Nginx deployment packaging.
- Overly generic CMS/page-builder abstractions.

## Existing Foundation

Phase 1 provides:

- Django project package: `config`.
- Foundation app: `core`.
- Environment-aware settings in `config/settings.py`.
- SQLite local fallback and PostgreSQL `DATABASE_URL` support.
- DRF and schema tooling, but no content APIs yet.
- pytest-django configuration and DRF APIClient smoke tests.

Phase 2 can build on this by adding apps to `INSTALLED_APPS`, adding migrations, and extending tests under each new app.

## Recommended Technical Approach

### App Layout

Use explicit Django apps by domain:

- `site_settings` - `CompanyProfile`, `SocialLink`, `CompanyStatistic`, `SiteMediaBanner`.
- `pages` - `WebsitePage` and optional page/banner association if needed.
- `content` - `TimelineEvent`, `TeamMember`, `ClientPartner`, `TestimonialDocument`, `Certification`, `Award`, `FAQ`.
- `catalog` - `ProductCategory`, `Product`, `Machinery`.
- `inquiries` - `ContactInquiry`, `JobApplication`.

This mirrors the planned domain boundaries while avoiding package names that collide with common imports such as `forms`.

### Shared Model Patterns

Recommended fields:

- `order = models.PositiveIntegerField(default=0, db_index=True)` for repeatable content.
- `is_active = models.BooleanField(default=True, db_index=True)` for content visibility.
- `created_at = models.DateTimeField(auto_now_add=True)` and `updated_at = models.DateTimeField(auto_now=True)` where auditability helps.
- `slug = models.SlugField(unique=True)` where routes/filtering need stable identifiers.

Recommended Meta patterns:

- `ordering = ["order", "id"]` for ordered repeatable content.
- `ordering = ["-created_at"]` for operational submissions.
- Index fields that will become common API filters in Phase 3, such as `is_active`, `slug`, `category`, `plant`, and `type`.

### Singleton Company Profile

`CompanyProfile` should behave as a singleton in admin:

- Enforce singleton in `clean()` or `save()` by preventing a second row.
- Admin should disable add permission when one row already exists.
- The model can include company/brand/contact fields, logo, address, phone/email, and optional website fields.

This avoids a dependency while keeping admin simple.

### Page and Banner Modeling

`WebsitePage` should represent known website pages with:

- `slug`
- `title`
- optional `meta_title`
- optional `meta_description`
- `order`
- `is_active`

`SiteMediaBanner` should include:

- optional page relation or page slug/placement field
- title/subtitle
- image/file
- optional video URL
- order
- is_active

This is enough for admin-managed page/banner content without implementing a section builder.

### Repeatable Content Modeling

Use one normalized model per repeatable content type:

- `TeamMember`: photo, full name, designation, bio, management pillar flag, order, is_active.
- `TimelineEvent`: year, title, description, order, is_active.
- `ClientPartner`: name/logo, order, is_active.
- `TestimonialDocument`: client/supplier name, document type, file/image, order, is_active.
- `Certification`: title, file/image, order, is_active.
- `Award`: title, file/image, order, is_active.
- `FAQ`: question, answer, order, is_active.

Avoid JSONField for these because their fields are known, searchable, and admin-editable.

### Catalog Modeling

Recommended catalog models:

- `ProductCategory`: name, slug, order, is_active.
- `Product`: category FK, name, slug, image, description, customer, specification, extra_details, order, is_active.
- `Machinery`: plant choice, name, image, total_machines, make, year_of_purchase, tonnage_or_capacity, platen_size_or_dimensions, order, is_active.

Use a constrained plant choice for Phase 2 (`plant_1`, `plant_2`) unless separate plant metadata becomes necessary. It satisfies plant separation with less admin overhead.

### Form Submission Modeling

`ContactInquiry`:

- name, email, phone, subject, message, source_page, created_at.
- Optional `status` can help admin review, but only add if it remains simple.

`JobApplication`:

- name, date of birth, address, city, contact number, email, qualifications, experience, area of interest, expected CTC, preferred contact date/time, created_at.
- No resume upload yet unless later confirmed.

Submission models should be visible/searchable/filterable in admin. Public write endpoints are Phase 3.

### Admin Design

Admin should be useful without becoming custom UI:

- `list_display`: include title/name, `is_active`, `order`, and relevant domain fields.
- `list_filter`: use `is_active`, type/category/plant, created dates.
- `search_fields`: title/name/question/email/phone/product fields as appropriate.
- `prepopulated_fields`: use for slug fields where the source is `name` or `title`.
- `ordering`: follow model ordering.
- `readonly_fields`: use timestamps and maybe simple file/link identifiers.
- Custom preview helpers can be added only if small and reliable.

### Testing Strategy

Use pytest-django and factory_boy/Faker already available from Phase 1:

- Model tests for required creation paths and string representations.
- Tests for singleton `CompanyProfile`.
- Tests for slug uniqueness where applicable.
- Tests for default `order`/`is_active` values and ordering.
- Tests for admin registrations using Django admin site registry.
- Optional tests for admin `list_display`, `search_fields`, and `list_filter` on key models.

## Risks and Mitigations

| Risk | Mitigation |
|------|------------|
| Phase 2 grows into a CMS/page builder | Use explicit models only; defer page sections and public APIs. |
| Too many apps make implementation noisy | Keep apps domain-based and small; do not add service layers. |
| Global singleton is accidentally duplicated | Add model/admin safeguards and tests. |
| Media fields become inconsistent | Use grouped upload paths and simple field names. |
| Form models leak into public reads | Add models/admin only now; no public API endpoints until Phase 3. |
| Admin is technically correct but hard to use | Include list displays, filters, search fields, ordering, and readable labels. |

## Validation Architecture

Phase 2 can be validated with deterministic local commands:

- `python manage.py makemigrations --check --dry-run` after migrations are committed.
- `python manage.py check`
- `python manage.py migrate --noinput`
- `pytest`

Plan-level verification should also assert:

- All Phase 2 apps appear in `INSTALLED_APPS`.
- Migrations exist for each new app with models.
- Admin registrations exist for all Phase 2 models.
- Tests cover singleton behavior, ordering/active defaults, slug behavior, and admin registrations.

## Plan Implications

Use three sequential plans:

1. Create domain apps, shared patterns, global/page models, admin, migrations, and tests.
2. Add repeatable content and catalog models, admin, migrations, and tests.
3. Add inquiry models plus cross-domain admin/test polish and final verification.

Sequential waves are safer because each plan updates shared Django settings, migrations, and model/admin test conventions. Parallel execution would risk migration and settings conflicts.
