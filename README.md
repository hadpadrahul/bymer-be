# Bymer Backend

Django + Django REST Framework backend for the Bymer company website. Staff manage content in the **`/dashboard/`** UI (or Django Admin for superusers); the frontend consumes stable JSON APIs.

## Branches

| Branch | Use |
|--------|-----|
| **`main`** | Clean app, docs, scripts — deploy from here. |
| **`development`** | Same + `.planning/` and project notes. Agent folders stay local only. [docs/BRANCHES.md](docs/BRANCHES.md). |

Local demo seed and API benchmark: [docs/DEVELOPMENT.md](docs/DEVELOPMENT.md).

## Quick start (local)

```powershell
python -m pip install -r requirements-dev.txt
Copy-Item .env.example .env
python manage.py migrate
python manage.py runserver
```

- Health: http://127.0.0.1:8000/api/health/
- API docs: http://127.0.0.1:8000/api/docs/
- Staff dashboard: http://127.0.0.1:8000/dashboard/
- Django Admin: http://127.0.0.1:8000/admin/

Environment variables are documented in `.env.example`. SQLite is the default when `DATABASE_URL` is empty; set `DATABASE_URL` for PostgreSQL.

## Documentation

| Doc | Contents |
|-----|----------|
| [docs/API.md](docs/API.md) | Endpoints, filters, page sections, forms |
| [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) | PythonAnywhere + VPS/Docker, backup/restore, smoke tests |
| [docs/BRANCHES.md](docs/BRANCHES.md) | What lives on `main` vs `development` |
| [docs/DEVELOPMENT.md](docs/DEVELOPMENT.md) | Demo seed, API benchmark, local workflow |
| [docs/ADMIN_DASHBOARD.md](docs/ADMIN_DASHBOARD.md) | Staff dashboard URLs, env vars, page sections |

## Tests

```powershell
pytest
```

## OpenAPI note

`/api/docs/` and `/api/schema/` are served by the running application. A `schema.yml` file on disk is **not** required for docs; it is only used optionally when validating the schema from the CLI (see DEVELOPMENT.md). That file is gitignored.
