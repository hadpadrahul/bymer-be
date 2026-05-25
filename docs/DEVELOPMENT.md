# Local development

Day-to-day setup, demo data, and API checks. Application code is the same on **`main`** and **`development`**; the latter also tracks `.planning/` and internal spec files (see [BRANCHES.md](./BRANCHES.md)).

## Setup

```powershell
python -m pip install -r requirements-dev.txt
Copy-Item .env.example .env
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

SQLite is used when `DATABASE_URL` is empty. Uploaded files go to `media/` (gitignored).

## OpenAPI / Swagger

- Swagger UI: http://127.0.0.1:8000/api/docs/
- Schema JSON: http://127.0.0.1:8000/api/schema/

The docs UI loads the schema from the running server. To validate the schema from the CLI (optional):

```powershell
python manage.py spectacular --file schema.yml --validate
```

`schema.yml` is a local artifact only (gitignored). Delete it after validation if you like.

## Demo content seeding

Populate the database with realistic demo records and placeholder images:

```powershell
python manage.py seed_demo_data --clear
```

| Flag | Effect |
|------|--------|
| `--clear` | Remove demo-tagged records first |
| `--no-images` | Text only, no file uploads |
| `--media-dir .\demo-media` | Use real images when present |

**Image basenames** in `--media-dir` (any of `.jpg`, `.jpeg`, `.png`, `.webp`):  
`logo`, `banner`, `team`, `client`, `testimonial`, `cert`, `award`, `product`, `machinery`.  
Missing files fall back to generated PNG placeholders.

Demo records use prefixes like `Demo `, `demo-`, or `@demo.bymer.local` so `--clear` can remove them safely.

## API benchmark

With `runserver` running in another terminal:

```powershell
python manage.py benchmark_apis
python manage.py benchmark_apis --rounds 3
```

Prints per-endpoint status, latency, response size, item counts, and fetches every media URL found in JSON responses.

| Flag | Effect |
|------|--------|
| `--skip-media` | Skip downloading media files |
| `--skip-write` | Skip contact/career POST tests |
| `--base-url` | Default `http://127.0.0.1:8000` |

## Tests

```powershell
pytest
```

## Before merging to `main`

1. `pytest` passes.
2. `python manage.py spectacular --file schema.yml --validate` passes.
3. Review [DEPLOYMENT.md](./DEPLOYMENT.md) pre-deploy checklist.
4. Ensure [API.md](./API.md) still matches any endpoint changes.

## API details

See [API.md](./API.md) for paths, filters, and page section mapping.
