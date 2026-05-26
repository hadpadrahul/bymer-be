# Production deployment

Deploy from the **`main`** branch only. Use **`development`** for ongoing work (includes `.planning/`).

| Target | Database | Typical use |
|--------|----------|-------------|
| **PythonAnywhere** | SQLite | Staging, demos, your first live test |
| **VPS + Docker** | PostgreSQL | Production |

Copy `.env.example` → `.env` and enable the block that matches your target.

---

## Pre-deploy checklist (any environment)

```bash
python -m pip install -r requirements.txt
python manage.py migrate --noinput
python manage.py collectstatic --noinput
pytest
python manage.py spectacular --file schema.yml --validate
```

Create a staff user for the dashboard:

```bash
python manage.py createsuperuser
# Set is_staff=True when prompted (superuser implies staff)
```

| Variable | Production |
|----------|------------|
| `DJANGO_SECRET_KEY` | Long random string (required) |
| `DJANGO_DEBUG` | `False` |
| `DJANGO_ALLOWED_HOSTS` | Your API hostname(s), comma-separated |
| `DATABASE_URL` | See PA vs VPS sections below |
| `DJANGO_CORS_ALLOWED_ORIGINS` | Frontend origin(s), HTTPS in production |
| `DJANGO_CSRF_TRUSTED_ORIGINS` | Same-site origins that POST to Django (dashboard, admin); include your API host if needed |
| `PUBLIC_WEBSITE_BASE_URL` | Marketing site URL (preview links in dashboard) |
| `ADMIN_NOTIFICATION_EMAILS` | Comma-separated inbox for form alerts |
| `DJANGO_SECURE_SSL_REDIRECT` | `False` behind Nginx/PA TLS; `True` only if Django terminates HTTPS directly |

`schema.yml` from `spectacular --validate` is optional and gitignored. `/api/docs/` uses the live `/api/schema/` endpoint.

---

## PythonAnywhere (SQLite)

Good for a **first deployment** without managing PostgreSQL.

### 1. Deploy code

On PA, in a Bash console:

```bash
cd ~
git clone <your-repo-url> bymer-be
cd bymer-be
git checkout main
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env — use the PythonAnywhere block in .env.example
```

Example `.env` values:

```env
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=YOURUSER.pythonanywhere.com
DATABASE_URL=sqlite:////home/YOURUSER/bymer-be/db.sqlite3
DJANGO_CORS_ALLOWED_ORIGINS=https://YOURUSER.pythonanywhere.com
DJANGO_CSRF_TRUSTED_ORIGINS=https://YOURUSER.pythonanywhere.com
```

### 2. Initialize

```bash
python manage.py migrate --noinput
python manage.py collectstatic --noinput
python manage.py createsuperuser
```

Optional demo data (staging only):

```bash
python manage.py seed_demo_data
```

### 3. WSGI

Web tab → **WSGI configuration file**. Point Django at your project (see `deploy/pythonanywhere_wsgi.py.sample`).

Reload the web app after changes.

### 4. Static and media mappings

Web tab → **Static files**:

| URL | Directory |
|-----|-----------|
| `/static/` | `/home/YOURUSER/bymer-be/staticfiles/` |
| `/media/` | `/home/YOURUSER/bymer-be/media/` |

Whitenoise also serves `/static/` through Django; the PA mapping is recommended so static assets are served efficiently.

### 5. Email (optional)

Set SMTP variables in `.env` (see `.env.example`) so `ADMIN_NOTIFICATION_EMAILS` receives contact/career alerts.

### 6. Post-deploy smoke (PA)

| Check | URL / action |
|-------|----------------|
| Health | `GET https://YOURUSER.pythonanywhere.com/api/health/` |
| API docs | `https://YOURUSER.pythonanywhere.com/api/docs/` |
| Dashboard login | `https://YOURUSER.pythonanywhere.com/dashboard/login/` |
| Staff CRUD | Open one list (e.g. Team), save a row |
| Public API | `GET /api/globals/company-profile/` |
| Forms | `POST /api/forms/contact/` with valid JSON → `201` |
| Media | Upload in dashboard; open file URL under `/media/` |

**PA limits:** SQLite is not ideal for high traffic; move to VPS + PostgreSQL when you outgrow PA.

---

## VPS with Docker + PostgreSQL

### 1. Prepare environment

On the server:

```bash
git clone <your-repo-url> /var/www/bymer
cd /var/www/bymer
git checkout main
cp .env.example .env
```

Edit `.env` using the **VPS / Docker** block. Set strong `DJANGO_SECRET_KEY` and real hostnames.

`docker-compose.yml` sets `DATABASE_URL=postgres://bymer:bymer@db:5432/bymer` for the web service. Change the Postgres password in compose and `.env` for production.

### 2. Build and run

```bash
docker compose up -d --build
docker compose exec web python manage.py createsuperuser
```

Gunicorn listens on port **8000** inside the container. The entrypoint runs **migrate** and **collectstatic** on each start.

### 3. Nginx on the host

1. Copy `deploy/nginx-bymer.conf` to `/etc/nginx/sites-available/bymer`.
2. Set `server_name`, TLS certificate paths, and aliases:
   - `/var/www/bymer/staticfiles/` (run `docker compose exec web python manage.py collectstatic` or copy from the container volume)
   - `/var/www/bymer/media/` — bind-mount or sync from the `media_data` volume
3. Enable the site and reload Nginx.

For media persistence, either:

- Mount host `/var/www/bymer/media` into the container in `docker-compose.yml`, or  
- Back up the `media_data` Docker volume regularly (see below).

### 4. Gunicorn without Docker (optional)

```bash
source .venv/bin/activate
gunicorn -c deploy/gunicorn.conf.py
```

Use systemd to keep Gunicorn running; Nginx proxies to `127.0.0.1:8000`.

---

## Static and media

| Asset | Development | Production |
|-------|-------------|------------|
| **Static** | Whitenoise + `collectstatic` → `staticfiles/` | Same; Nginx can also serve `/static/` |
| **Media** | `media/` under project root | Serve `/media/` via Nginx (VPS) or PA static mapping; never use `runserver` |

`client_max_body_size` in Nginx should allow your largest upload (dashboard default 10 MB).

---

## Backup

Back up **database** and **media** together. Restoring only one leads to broken image links or orphaned files.

### PythonAnywhere (SQLite)

```bash
# From a PA Bash console — adjust paths and backup destination
cp /home/YOURUSER/bymer-be/db.sqlite3 ~/backups/bymer-$(date +%F).sqlite3
tar -czf ~/backups/bymer-media-$(date +%F).tar.gz -C /home/YOURUSER/bymer-be media
```

Download backups off PA periodically (Files tab or `scp`).

### VPS (PostgreSQL + media)

```bash
# Database dump
docker compose exec -T db pg_dump -U bymer bymer > ~/backups/bymer-$(date +%F).sql

# Media (if using named volume)
docker run --rm -v bymer_media_data:/data -v ~/backups:/backup alpine \
  tar -czf /backup/bymer-media-$(date +%F).tar.gz -C /data .
```

Or from a host bind-mount:

```bash
tar -czf ~/backups/bymer-media-$(date +%F).tar.gz -C /var/www/bymer media
```

**Schedule:** daily DB + media; keep at least 7 daily and 4 weekly off-server.

---

## Restore

### PythonAnywhere

1. Stop the web app (Web tab → disable or reload after files are in place).
2. Replace `db.sqlite3` with the backup copy.
3. Extract media archive into project `media/` (merge, do not delete unrelated files if unsure).
4. `python manage.py migrate --noinput` (applies any newer migrations safely).
5. Reload the web app.
6. Run the [smoke checks](#post-deploy-smoke-pa) below.

### VPS (PostgreSQL)

1. `docker compose down` (or stop Gunicorn only if not using compose).
2. Restore database:
   ```bash
   cat ~/backups/bymer-YYYY-MM-DD.sql | docker compose exec -T db psql -U bymer bymer
   ```
   For a clean restore into an empty DB, drop/recreate the database first.
3. Restore media volume or `media/` directory from tarball.
4. `docker compose up -d`
5. `docker compose exec web python manage.py migrate --noinput`
6. Run smoke checks.

### After any restore

- Verify `DJANGO_SECRET_KEY` and `.env` match the environment you backed up.
- Re-run smoke tests, especially `/api/health/`, a media URL, and `/dashboard/login/`.

---

## Post-deploy smoke (all environments)

| Check | Expected |
|-------|----------|
| `GET /api/health/` | `200` |
| `GET /api/schema/` | `200` |
| `/api/docs/` | Swagger loads |
| `GET /api/globals/company-profile/` | `200` JSON |
| `/dashboard/login/` | Login as staff → home |
| Dashboard | One edit + save (e.g. FAQ or company profile) |
| `POST /api/forms/contact/` | `201` (valid payload) |
| CORS | Browser call from frontend origin succeeds |
| Media | Uploaded file opens at `/media/...` |

---

## Security

- `DEBUG=False` in production.
- Restrict `/admin/` by network or strong passwords; editors should use `/dashboard/`.
- Rotate `DJANGO_SECRET_KEY` if leaked.
- Update dependencies: `pip install -r requirements.txt -U` on a schedule.

---

## Branch workflow

| Branch | Deploy? |
|--------|---------|
| `main` | Yes |
| `development` | No — merge to `main` first ([BRANCHES.md](./BRANCHES.md)) |

---

## Related docs

- [DEVELOPMENT.md](./DEVELOPMENT.md) — local setup, seed, benchmark  
- [ADMIN_DASHBOARD.md](./ADMIN_DASHBOARD.md) — staff UI  
- [API.md](./API.md) — public API contract  
- `deploy/nginx-bymer.conf`, `deploy/gunicorn.conf.py`, `docker-compose.yml`
