# Production deployment

Use this checklist when deploying from the **`main`** branch (application code only, no demo seeding tools required on the server).

> Docker, `docker-compose`, and Nginx sample configs are planned as part of the next deployment packaging work. Until those files exist in the repo, follow the process below with your own process manager and reverse proxy.

## Branch roles

| Branch | Purpose |
|--------|---------|
| **`main`** | Production-ready application code. Merge here when tests pass and docs match the release. |
| **`development`** | Active work, local demo seeding, API benchmark commands, and extra docs for integrators. |

## Environment variables

Copy `.env.example` to `.env` on the server and set:

| Variable | Production |
|----------|------------|
| `DJANGO_SECRET_KEY` | Long random secret (required) |
| `DJANGO_DEBUG` | `False` |
| `DJANGO_ALLOWED_HOSTS` | Your domain(s), comma-separated |
| `DATABASE_URL` | PostgreSQL URL, e.g. `postgres://user:pass@host:5432/dbname` |
| `DJANGO_CORS_ALLOWED_ORIGINS` | Frontend origin(s), e.g. `https://www.example.com` |

Leave `DATABASE_URL` empty only for local SQLite testing — not for VPS production.

## Pre-deploy verification (run on the release commit)

```bash
python -m pip install -r requirements.txt
python manage.py migrate --noinput
python manage.py collectstatic --noinput
pytest
python manage.py spectacular --file schema.yml --validate
```

- **`schema.yml`:** Generated only for this validation step. It is gitignored. Swagger at `/api/docs/` uses the live `/api/schema/` endpoint — you do not need to ship `schema.yml` to the server.
- Delete `schema.yml` after validation if you do not want it on disk.

## Runtime (typical VPS)

1. **Application:** Gunicorn (or similar) pointing at `config.wsgi:application`.
2. **Static files:** Run `collectstatic`; serve `STATIC_ROOT` via Whitenoise inside the app and/or Nginx at `/static/`.
3. **Media uploads:** Serve `MEDIA_ROOT` at `/media/` via Nginx (recommended). Do not rely on Django `runserver` in production.
4. **Database:** PostgreSQL with backups enabled.
5. **HTTPS:** Terminate TLS at Nginx or your load balancer; set `DJANGO_ALLOWED_HOSTS` and CORS to HTTPS origins.

## Post-deploy smoke checks

| Check | How |
|-------|-----|
| Health | `GET https://<host>/api/health/` → `200` |
| Schema | `GET https://<host>/api/schema/` → `200` |
| Docs | Open `https://<host>/api/docs/` |
| Globals | `GET https://<host>/api/globals/company-profile/` |
| Page | `GET https://<host>/api/pages/home/` (after content exists in admin) |
| Media | Open an `*_url` from an API response; should load over HTTPS |
| Forms | `POST` contact/career with valid JSON → `201`; confirm rows in admin |
| Admin | `https://<host>/admin/` login works |
| CORS | Frontend origin can call APIs from the browser |

## Media backup

Uploaded files live under `MEDIA_ROOT` (default: project `media/` directory). Back up that directory with the database; restores need both to stay in sync.

## Security reminders

- `DEBUG=False` in production.
- Restrict admin URL or protect with network rules if needed.
- Rotate `DJANGO_SECRET_KEY` if compromised.
- Keep dependencies updated (`requirements.txt`).

## What is not on `main` by design

Demo helpers (`seed_demo_data`, `benchmark_apis`) live in `core/management/` and are intended for **`development`** branch local testing. They are safe to run on a staging copy of production data only if you understand they create or clear demo-tagged records.
