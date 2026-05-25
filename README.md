# Bymer Backend

Django + Django REST Framework backend for the Bymer company website. Admins manage content in Django Admin; the frontend consumes stable JSON APIs.

## Branches

| Branch | Use |
|--------|-----|
| **`main`** | Production-ready app code. Deploy from here. See [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md). |
| **`development`** | Active development, demo seeding, and API benchmarks. See [docs/DEVELOPMENT.md](docs/DEVELOPMENT.md). |

## Quick start (local)

```powershell
python -m pip install -r requirements-dev.txt
Copy-Item .env.example .env
python manage.py migrate
python manage.py runserver
```

- Health: http://127.0.0.1:8000/api/health/
- API docs: http://127.0.0.1:8000/api/docs/
- Admin: http://127.0.0.1:8000/admin/

Environment variables are documented in `.env.example`. SQLite is the default when `DATABASE_URL` is empty; set `DATABASE_URL` for PostgreSQL.

## Documentation

| Doc | Contents |
|-----|----------|
| [docs/API.md](docs/API.md) | Endpoints, filters, page sections, forms |
| [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) | VPS checklist, env vars, smoke tests, media backup |
| [docs/DEVELOPMENT.md](docs/DEVELOPMENT.md) | Demo seed, API benchmark, local workflow |

## Tests

```powershell
pytest
```

## OpenAPI note

`/api/docs/` and `/api/schema/` are served by the running application. A `schema.yml` file on disk is **not** required for docs; it is only used optionally when validating the schema from the CLI (see DEVELOPMENT.md). That file is gitignored.
