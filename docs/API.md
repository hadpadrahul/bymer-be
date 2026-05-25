# API reference

Base path: `/api/`

All public read endpoints return only active records, ordered by `order` then name/title. List endpoints are paginated (page size 50) unless noted.

Interactive docs: `/api/docs/` (Swagger UI). OpenAPI JSON: `/api/schema/` — served live by the app; no static `schema.yml` file is required.

## Health

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/health/` | Simple health check |

## Globals (`/api/globals/`)

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/globals/company-profile/` | Single company profile (logo, contact, tagline) |
| GET | `/api/globals/social-links/` | Active social links |
| GET | `/api/globals/statistics/` | Active headline statistics |
| GET | `/api/globals/banners/` | Active site banners |

## Content (`/api/content/`)

| Method | Path | Query params |
|--------|------|----------------|
| GET | `/api/content/team/` | `?pillar=true` — management pillar only |
| GET | `/api/content/timelines/` | |
| GET | `/api/content/clients/` | |
| GET | `/api/content/testimonials/` | `?type=customer` or `?type=supplier` |
| GET | `/api/content/certifications/` | |
| GET | `/api/content/awards/` | |
| GET | `/api/content/faqs/` | |

## Catalog (`/api/catalog/`)

| Method | Path | Query params |
|--------|------|----------------|
| GET | `/api/catalog/categories/` | |
| GET | `/api/catalog/products/` | `?category=<category-slug>` |
| GET | `/api/catalog/machinery/` | `?plant=plant_1` or `?plant=plant_2` |

## Pages (`/api/pages/`)

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/pages/<slug>/` | Page metadata, optional `banners`, and `sections` |

Inactive or unknown slugs return `404`.

**Section types by slug** (only non-empty sections are returned):

| Slug | Sections |
|------|----------|
| `home` | `statistics` |
| `our-team` | `team` |
| `our-history` | `timelines` |
| `testimonials` | `testimonials` |
| `quality-assurance` | `certifications`, `awards` |
| `automotive-products`, `non-automotive-products` | `products` (filtered by category slug) |
| `machinery` | `machinery` |
| `contact-us` | `faqs` |

**Banners:** Each page response can include `banners` for banners linked to that page or global banners (no page set). Use `/api/globals/banners/` if you only need the global list.

## Forms (`/api/forms/`) — write only

| Method | Path | Status |
|--------|------|--------|
| POST | `/api/forms/contact/` | `201` on success |
| POST | `/api/forms/career/` | `201` on success |

GET (and other methods) on these URLs return `405`. There is no public API to list submissions.

**Contact body:** `name`, `email`, `phone`, `subject`, `message`, `source_page` (all required except where model allows blank).

**Career body:** `full_name`, `address`, `contact_number`, `email`, `qualifications` required; optional: `date_of_birth`, `city`, `experience`, `area_of_interest`, `expected_ctc`, `preferred_contact_datetime`.

## Media URLs

Image and file fields are returned as absolute URLs (e.g. `logo_url`, `image_url`, `photo_url`) when a file is uploaded. Empty uploads are omitted or `null`.

In local `DEBUG` mode, files are served from `/media/...` by Django. In production, Nginx (or equivalent) should serve `MEDIA_ROOT` at `MEDIA_URL`.

## Admin

Content is managed at `/admin/`. Create a superuser with `python manage.py createsuperuser`.
