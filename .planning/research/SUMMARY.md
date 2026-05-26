# Research Summary

## Stack

Use Django 5.2 LTS, Django REST Framework, PostgreSQL in production, SQLite locally, Docker, Gunicorn, Nginx, Whitenoise, `django-environ`, `django-cors-headers`, `django-filter`, `drf-spectacular`, and Pillow. Add pytest tooling from the start.

The stack should be boring and durable. Django Admin is the main reason to choose Django here; DRF provides the predictable frontend contract.

## Table Stakes

- Admin-managed global content, page content, repeatable content, catalog content, credibility content, and form submissions.
- Stable REST endpoints with page-centric and collection styles.
- Ordering, active flags, filtering, pagination where needed, lean serializers, and generated OpenAPI schema.
- Production-ready settings, static/media handling, Docker deployment assumptions, and documentation.

## Differentiators

- A pragmatic `GET /api/pages/<slug>/` endpoint that gives the frontend page-ready data without becoming a generic page builder.
- Admin polish for non-technical editors.
- Query-conscious implementation from the beginning.
- Clear API examples so frontend integration does not guess.

## Watch Out For

- Do not turn the data model into a generic CMS.
- Do not under-invest in admin usability.
- Do not create endpoint sprawl.
- Do not put DB queries in serializers.
- Do not leave media/static production behavior ambiguous.

## Recommended Roadmap Shape

Use vertical MVP phases:

1. Backend foundation and content conventions.
2. Admin-managed content models for globals, content, catalog, and forms.
3. Public API contract, serializers, filters, schema, and page assembly.
4. Production readiness, tests, documentation, and deployment packaging.

This keeps the app useful quickly while still validating the highest-risk decisions before adding deployment polish.
