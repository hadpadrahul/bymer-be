# Staff content dashboard

Private UI for editors at **`/dashboard/`** (Django templates, Tailwind CDN, HTMX, minimal Alpine). Django Admin at `/admin/` remains available for superusers.

## Access

1. Create a user with **Staff status** (`is_staff=True`) via `createsuperuser` or Django Admin.
2. Open http://127.0.0.1:8000/dashboard/login/
3. Session cookie auth; logout clears the session.

Non-staff users get HTTP 403 on dashboard routes.

## What editors can do

| Area | URL pattern | Notes |
|------|-------------|--------|
| Home | `/dashboard/` | Counts, content warnings, recent submissions |
| Company profile | `/dashboard/globals/profile/` | Singleton |
| Pages | `/dashboard/pages/` | Meta CRUD; sections are code-mapped (read-only table + links) |
| Globals | `/dashboard/manage/social-links/` etc. | Social links, statistics, banners |
| Content | `/dashboard/manage/team/` etc. | Team, timeline, clients, testimonials, certs, awards, FAQs |
| Catalog | `/dashboard/manage/categories/` etc. | Categories, products, machinery |
| Inbox | `/dashboard/inquiries/contact/` | Status + internal notes; CSV export; no delete |
| Media | `/dashboard/media/` | Upload library files (reference URLs when editing content) |
| API reference | `/dashboard/api-reference/` | Public endpoint list + link to Swagger |
| Audit log | `/dashboard/audit-log/` | Recent staff actions |

## Admin JSON API (`/api/admin/`)

Staff session required (`IsAdminUser`). Used for HTMX/AJAX helpers:

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/admin/health/` | GET | Session check |
| `/api/admin/<registry_key>/<id>/toggle-active/` | PATCH | Flip `is_active` |
| `/api/admin/<registry_key>/<id>/order/` | PATCH | Set `order` |

Registry keys match list URLs (e.g. `team`, `products`, `banners`).

Public **`/api/`** is unchanged for the marketing frontend.

## Environment variables

| Variable | Purpose |
|----------|---------|
| `ADMIN_NOTIFICATION_EMAILS` | Comma-separated emails for new contact/career submissions |
| `PUBLIC_WEBSITE_BASE_URL` | Optional preview links on page detail (e.g. `https://www.example.com`) |
| `DASHBOARD_MAX_UPLOAD_MB` | Documented limit; forms enforce 10 MB on media upload |

## Page sections (important)

Page composition is defined in `pages/page_compose.py`, not in the database. The dashboard shows which section types apply to each slug and links to the relevant collection CRUD screens. Reordering section types on a page requires a code change and deploy.

## Email on new submissions

When `ADMIN_NOTIFICATION_EMAILS` is set, creating a contact or career submission via the public API sends a plain-text email with a link to the dashboard detail view.

## Tests

```powershell
pytest dashboard/tests/
```

See also [DEVELOPMENT.md](./DEVELOPMENT.md).
