# Stack Research

## Recommendation

Use a conventional Django 5.2 LTS + Django REST Framework backend with PostgreSQL in production, SQLite for local development, and Docker/Nginx/Gunicorn for deployment. This matches the admin-first content workflow and keeps the backend maintainable without inventing a CMS layer.

## Core Runtime

- **Python**: Use a current Python version supported by Django 5.2, preferably Python 3.12 or 3.13 during setup.
- **Django**: Use Django 5.2 LTS. It is the safest default for a production site because it receives security support through April 2028.
- **Django REST Framework**: Use the current stable DRF release family. As of May 2026, DRF 3.17.1 is published; confirm compatibility in the lock file when installing.
- **Database**: SQLite locally, PostgreSQL in production.
- **Server**: Gunicorn behind Nginx.
- **Static files**: Whitenoise for app static assets, with Nginx serving collected static and uploaded media in production.

## Project Libraries

Recommended initial dependencies:

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

Recommended test dependencies:

- `pytest`
- `pytest-django`
- `factory_boy`
- `Faker`

## Optional Later

- `drf-spectacular-sidecar` only if self-hosted Swagger/ReDoc assets are needed.
- Email backend/provider package only when notification emails are confirmed.
- Dedicated object storage client only if uploaded media moves away from VPS disk.

## What Not To Use

- Wagtail or a full CMS: too broad for the one-site admin-first scope.
- Django CMS/page builders: unnecessary abstraction and higher maintenance.
- Celery: not needed unless async email, media processing, or scheduled jobs become real requirements.
- GraphQL: the frontend contract is straightforward REST with page and collection endpoints.

## Confidence

High. This stack directly fits a small, read-heavy, admin-managed company website and keeps deployment familiar.
