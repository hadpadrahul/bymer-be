# Bymer Backend

Lightweight Django + Django REST Framework backend for the Bymer dynamic website.

## Prerequisites

- Python 3.12+
- Existing virtual environment at `C:\Users\rahul\Desktop\bymer-be\.venv`

## Local Setup

Activate the virtual environment:

```powershell
& "C:\Users\rahul\Desktop\bymer-be\.venv\Scripts\Activate.ps1"
```

Install development dependencies:

```powershell
python -m pip install -r requirements-dev.txt
```

Create a local environment file:

```powershell
Copy-Item .env.example .env
```

Local development uses SQLite by default when `DATABASE_URL` is empty. Production can point `DATABASE_URL` at PostgreSQL without code changes.

Run migrations:

```powershell
python manage.py migrate
```

Start the development server:

```powershell
python manage.py runserver
```

## API

- Health check: `/api/health/`
- OpenAPI schema: `/api/schema/`
- Swagger UI: `/api/docs/`

## Tests

```powershell
pytest
```

## Static and Media

Static files use `STATIC_URL` and `STATIC_ROOT`. Uploaded media uses `MEDIA_URL` and `MEDIA_ROOT`. Later deployment work will wire these paths to the VPS/Nginx static and media serving setup.
