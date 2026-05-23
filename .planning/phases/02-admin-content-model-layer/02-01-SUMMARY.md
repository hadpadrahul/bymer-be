# Plan 02-01 Summary: Global and Page Admin Models

## Status

Complete - 2026-05-23

## Objective

Create Django apps, models, migrations, admin classes, and tests for global/site-wide content plus known page records and page-linked banner content.

## Completed Tasks

### T1 - Create global/page app scaffolds

- Added `site_settings` and `pages` app packages.
- Added both apps to `INSTALLED_APPS`.
- Created migrations and test package initializers.
- Verification: `python manage.py check` passed.
- Commit: `3839c9f feat(02-01): scaffold global page apps`

### T2 - Add singleton and repeatable global content models

- Added `CompanyProfile`, `SocialLink`, and `CompanyStatistic`.
- Enforced singleton `CompanyProfile` behavior with model validation.
- Added model tests for singleton behavior, defaults, and string representations.
- Generated `site_settings/migrations/0001_initial.py`.
- Verification: `python manage.py check` and `pytest site_settings/tests/test_models.py` passed.
- Commit: `b93c5ef feat(02-01): add global content models`

### T3 - Add known page and banner models with migrations

- Added `WebsitePage` with unique slugs, ordering, active flag, and metadata fields.
- Added `SiteMediaBanner` with optional `WebsitePage` association, media fields, ordering, and active flag.
- Generated `pages/migrations/0001_initial.py` and `site_settings/migrations/0002_sitemediabanner.py`.
- Added model tests for page slug uniqueness, ordering, defaults, and banner association.
- Verification: `python manage.py makemigrations --check --dry-run`, `python manage.py migrate --noinput`, and model tests passed.
- Commit: `06d5127 feat(02-01): add page banner models`

### T4 - Register global/page models in admin

- Registered all `site_settings` models and `WebsitePage` in Django Admin.
- Added list displays, filters, search fields, ordering, slug prepopulation, and timestamp readonly fields.
- Added `CompanyProfileAdmin.has_add_permission()` to prevent a second profile in admin.
- Added admin registration/configuration tests.
- Verification: `pytest site_settings/tests/test_admin.py pages/tests/test_admin.py`, `python manage.py check`, `python manage.py makemigrations --check --dry-run`, `python manage.py migrate --noinput`, and `pytest site_settings pages` passed.
- Commit: `92b0c84 feat(02-01): register global page admin`

## Verification

- `python manage.py makemigrations --check --dry-run` - PASS
- `python manage.py check` - PASS
- `python manage.py migrate --noinput` - PASS
- `pytest site_settings pages` - PASS

## Requirements Covered

- ADMIN-01, ADMIN-02, ADMIN-03, ADMIN-04, ADMIN-05
- GLOB-01, GLOB-02, GLOB-03, GLOB-04
- PAGE-01, PAGE-02

## Deviations from Plan

None.

## Self-Check: PASSED

The global/page model layer is installed, migrated, admin-manageable, tested, and does not add public DRF serializers, routers, URLs, or endpoints.
